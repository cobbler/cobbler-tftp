"""
Tests for the TFTP server module, focused on the invalid-token
re-authentication retry logic in ``CobblerRequestHandler.get_response_data``
and the related ``TFTPServer`` token renewal / handler wiring.
"""

import time
import xmlrpc.client
from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest

from cobbler_tftp.server.tftp import (
    CobblerRequestHandler,
    CobblerResponseData,
    FileResponseData,
    TFTPServer,
    _is_invalid_token_fault,
)

if TYPE_CHECKING:
    import pytest_mock


@pytest.fixture
def settings() -> MagicMock:
    """
    Fixture providing a stand-in for a ``Settings`` object with just the
    attributes touched by the code under test.
    """
    fake_settings = MagicMock()
    fake_settings.prefetch_size = 65536
    fake_settings.static_fallback_dir = None
    fake_settings.user = "cobbler"
    fake_settings.password = "cobbler"
    fake_settings.uri = "http://localhost/cobbler_api"
    fake_settings.token_refresh_interval = 1800
    return fake_settings


@pytest.fixture
def handler(settings: MagicMock) -> CobblerRequestHandler:
    """
    Fixture providing a bare ``CobblerRequestHandler`` built via ``__new__``,
    bypassing ``BaseHandler.__init__`` (which would otherwise parse options
    and immediately call ``get_response_data`` itself).
    """
    bare_handler = CobblerRequestHandler.__new__(CobblerRequestHandler)
    bare_handler._api = MagicMock()
    bare_handler._token = "old-token"
    bare_handler._path = "boot/pxelinux.0"
    bare_handler._settings = settings
    bare_handler._reauth = MagicMock(return_value="new-token")
    return bare_handler


@pytest.fixture
def server(settings: MagicMock) -> TFTPServer:
    """
    Fixture providing a bare ``TFTPServer`` built via ``__new__``, bypassing
    ``BaseServer.__init__`` (which would otherwise bind a real UDP socket).
    """
    bare_server = TFTPServer.__new__(TFTPServer)
    bare_server._settings = settings
    bare_server._token = None
    bare_server._token_renew_time = 0.0
    return bare_server


def test_is_invalid_token_fault_true_for_invalid_token_message():
    fault = xmlrpc.client.Fault(
        1, "<class 'cobbler.cexceptions.CX'>:invalid token: abc123"
    )

    assert _is_invalid_token_fault(fault) is True


def test_is_invalid_token_fault_false_for_unrelated_fault():
    fault = xmlrpc.client.Fault(1, "<class 'FileNotFoundError'>:/some/path")

    assert _is_invalid_token_fault(fault) is False


def test_is_invalid_token_fault_true_for_quoted_token_value():
    """
    Regression guard for the exact faultString format observed live against a real cobblerd: the
    token value itself is wrapped in a single quote by cobblerd's own string formatting.
    """
    fault = xmlrpc.client.Fault(
        1, "<class 'cobbler.cexceptions.CX'>:'invalid token: abc123'"
    )

    assert _is_invalid_token_fault(fault) is True


def test_is_invalid_token_fault_false_for_unrelated_fault_containing_the_literal_text():
    """
    Security regression guard: a client-controlled TFTP request path containing the literal text
    "invalid token" must not be able to masquerade as a token-rejection fault via an unrelated
    error whose faultString happens to embed that path. A bare substring search would wrongly
    match this and trigger a pointless forced re-login; the anchored match must not.
    """
    fault = xmlrpc.client.Fault(
        1, "<class 'FileNotFoundError'>:/some/invalid token/path"
    )

    assert _is_invalid_token_fault(fault) is False


def test_is_invalid_token_fault_false_for_non_fault_error():
    error = xmlrpc.client.ProtocolError("host", 404, "msg", {})

    assert _is_invalid_token_fault(error) is False


def test_get_response_data_retries_once_on_invalid_token_and_succeeds(
    handler: CobblerRequestHandler,
):
    fault = xmlrpc.client.Fault(
        1, "<class 'cobbler.cexceptions.CX'>:invalid token: abc123"
    )
    file_contents = b"filedata"
    binary = xmlrpc.client.Binary(file_contents)
    handler._api.get_tftp_file.side_effect = [fault, (binary, len(file_contents))]  # type: ignore[attr-defined]

    resp = handler.get_response_data()

    assert isinstance(resp, CobblerResponseData)
    assert resp.size() == len(file_contents)
    handler._reauth.assert_called_once()  # type: ignore[attr-defined]
    assert handler._api.get_tftp_file.call_count == 2  # type: ignore[attr-defined]
    second_call_token = handler._api.get_tftp_file.call_args_list[1].args[3]  # type: ignore[attr-defined]
    assert second_call_token == "new-token"
    assert handler._token == "new-token"


def test_get_response_data_falls_back_to_static_dir_if_retry_also_fails(
    handler: CobblerRequestHandler, tmp_path
):
    fault_one = xmlrpc.client.Fault(
        1, "<class 'cobbler.cexceptions.CX'>:invalid token: abc123"
    )
    fault_two = xmlrpc.client.Fault(
        1, "<class 'cobbler.cexceptions.CX'>:invalid token: xyz789"
    )
    handler._api.get_tftp_file.side_effect = [fault_one, fault_two]  # type: ignore[attr-defined]
    handler._settings.static_fallback_dir = tmp_path  # type: ignore[attr-defined]
    fallback_file = tmp_path / "boot" / "pxelinux.0"
    fallback_file.parent.mkdir(parents=True)
    fallback_file.write_bytes(b"static-content")

    resp = handler.get_response_data()

    try:
        assert isinstance(resp, FileResponseData)
        assert resp.size() == len(b"static-content")
    finally:
        resp.close()
    handler._reauth.assert_called_once()  # type: ignore[attr-defined]
    assert handler._api.get_tftp_file.call_count == 2  # type: ignore[attr-defined]


def test_get_response_data_reraises_if_retry_fails_and_no_fallback_dir(
    handler: CobblerRequestHandler,
):
    fault_one = xmlrpc.client.Fault(
        1, "<class 'cobbler.cexceptions.CX'>:invalid token: abc123"
    )
    fault_two = xmlrpc.client.Fault(
        1, "<class 'cobbler.cexceptions.CX'>:invalid token: xyz789"
    )
    handler._api.get_tftp_file.side_effect = [fault_one, fault_two]  # type: ignore[attr-defined]
    handler._settings.static_fallback_dir = None  # type: ignore[attr-defined]

    with pytest.raises(xmlrpc.client.Fault) as exc_info:
        handler.get_response_data()

    assert exc_info.value is fault_two
    handler._reauth.assert_called_once()  # type: ignore[attr-defined]


def test_get_response_data_does_not_reauth_on_unrelated_fault(
    handler: CobblerRequestHandler, tmp_path
):
    unrelated_fault = xmlrpc.client.Fault(1, "<class 'FileNotFoundError'>:/some/path")
    handler._api.get_tftp_file.side_effect = [unrelated_fault]  # type: ignore[attr-defined]
    handler._settings.static_fallback_dir = tmp_path  # type: ignore[attr-defined]
    fallback_file = tmp_path / "boot" / "pxelinux.0"
    fallback_file.parent.mkdir(parents=True)
    fallback_file.write_bytes(b"static-content")

    resp = handler.get_response_data()

    try:
        assert isinstance(resp, FileResponseData)
    finally:
        resp.close()
    handler._reauth.assert_not_called()  # type: ignore[attr-defined]
    assert handler._api.get_tftp_file.call_count == 1  # type: ignore[attr-defined]


def test_renew_token_forces_login_when_force_true_even_if_not_expired(
    server: TFTPServer,
):
    original_renew_time = time.monotonic() + 10_000
    server._token_renew_time = original_renew_time
    server._token = "stale-token"
    api = MagicMock()
    api.login.return_value = "fresh-token"

    server._renew_token(api, force=True)

    api.login.assert_called_once_with(server._settings.user, server._settings.password)
    assert server._token == "fresh-token"
    assert server._token_renew_time < original_renew_time


def test_renew_token_skips_login_when_not_expired_and_not_forced(server: TFTPServer):
    server._token_renew_time = time.monotonic() + 10_000
    server._token = "cached-token"
    api = MagicMock()

    server._renew_token(api)

    api.login.assert_not_called()
    assert server._token == "cached-token"


def test_get_handler_reauth_callback_updates_server_token(
    server: TFTPServer, mocker: "pytest_mock.MockerFixture"
):
    server._token = "old-token"
    original_renew_time = time.monotonic() + 10_000
    server._token_renew_time = original_renew_time

    mock_server_cls = mocker.patch("xmlrpc.client.Server")
    mock_api = mock_server_cls.return_value
    mock_api.login.return_value = "new-token"

    mock_handler_cls = mocker.patch("cobbler_tftp.server.tftp.CobblerRequestHandler")

    server.get_handler(("0.0.0.0", 69), ("1.2.3.4", 1234), "/boot/pxelinux.0", {})

    # The initial, non-forced renewal inside get_handler must not log in
    # again since the token has not expired yet.
    mock_api.login.assert_not_called()

    reauth = mock_handler_cls.call_args.args[-1]
    result = reauth()

    mock_api.login.assert_called_once_with(
        server._settings.user, server._settings.password
    )
    assert result == "new-token"
    assert server._token == "new-token"
    assert server._token_renew_time < original_renew_time
