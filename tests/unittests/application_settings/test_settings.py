"""
Tests for the application settings module.
"""

import os
from pathlib import Path
from unittest import mock

import pytest

from cobbler_tftp.settings import Settings, SettingsFactory


@pytest.fixture
def settings_factory():
    """
    Fixture that represends the SettingsFactory class
    """
    return SettingsFactory()


def assert_default_settings(settings):
    assert settings.auto_migrate_settings is False
    assert settings.is_daemon is True
    assert str(settings.pid_file_path) == "/run/cobbler-tftp.pid"
    assert settings.uri == "http://localhost/cobbler_api"
    assert settings.user == "cobbler"
    assert settings.password == "cobbler"
    assert settings.tftp_addr == "127.0.0.1"
    assert settings.tftp_port == 69
    assert settings.tftp_retries == 5
    assert settings.tftp_timeout == 2
    assert str(settings.logging_conf) == "/etc/cobbler-tftp/logging.conf"


def assert_customized_settings(settings):
    assert settings.auto_migrate_settings is True
    assert settings.is_daemon is False
    assert settings.uri == "http://testmachine.testnetwork.com/api"
    assert settings.user == "cobbler"
    assert settings.password == "password"
    assert settings.tftp_addr == "0.0.0.0"  # nosec
    assert settings.tftp_port == 1969
    assert settings.tftp_retries == 10
    assert settings.tftp_timeout == 3


def test_build_settings_with_default_config_file(
    settings_factory: SettingsFactory, mocker
):
    """
    Test the ``build_settings`` function without passing a config file path or additional arguments.

    :assert: True if build successfull and the values of the Settings object correspond to the values inside the default
             config file
    """
    # Call the build_settings method with None as the config_path argument
    settings = settings_factory.build_settings(None)

    # Assert that the expected values are set in the Settings object
    assert isinstance(settings, Settings)
    assert_default_settings(settings)


def test_build_settings_with_valid_config_file(
    settings_factory: SettingsFactory, mocker
):
    valid_file_path = Path("tests/test_data/valid_config.yml")
    settings = settings_factory.build_settings(valid_file_path)

    assert isinstance(settings, Settings)
    assert_customized_settings(settings)


def test_build_settings_with_absolute_config_path(
    settings_factory: SettingsFactory, mocker
):
    absolute_path = Path("tests/test_data/valid_config.yml").absolute()
    settings = settings_factory.build_settings(absolute_path)

    assert isinstance(settings, Settings)
    assert_customized_settings(settings)


def test_build_settings_with_invalid_config_file(
    settings_factory: SettingsFactory, mocker
):
    # Pass path to invalid yaml file in /test_data/invalid_config.yml
    # Assert that YAMLError gets raised
    path = Path("tests/test_data/invalid_config.yml")

    with pytest.raises(ValueError) as exc:
        settings_factory.build_settings(path)

    assert """Validation Error: Configuration Parameters could not be validated!\n
                This may be due to an invalid configuration file or path.""" in str(
        exc.value
    )


def test_build_settings_with_missing_config_file(
    settings_factory: SettingsFactory, capsys
):
    """
    Test the ``build_settings`` function while passing it a path without a config file present.
    Should return a ``Settings`` object with default parameters.

    :assert: Whether a Settings object is built, it contains all default parameters and a stdout with a warning
             is printed
    """
    # Arrange
    path = Path("tests/test_data/missing_file.yml")
    expected_message = f"Warning: No configuration file found at {path}! Using default configuration file...\n"

    # Act
    settings = settings_factory.build_settings(path)

    # Assert
    captured_message = capsys.readouterr()
    assert captured_message.out == expected_message
    assert isinstance(settings, Settings)
    assert_default_settings(settings)


def test_build_settings_with_cli_args(settings_factory: SettingsFactory):
    cli_settings = ["tftp.address=1.2.3.4"]

    settings = settings_factory.build_settings(None, cli_arguments=cli_settings)

    assert isinstance(settings, Settings)
    assert settings.tftp_addr == "1.2.3.4"


def test_build_settings_with_integer_cli_args(settings_factory: SettingsFactory):
    cli_settings = ["tftp.port=1969"]

    settings = settings_factory.build_settings(None, cli_arguments=cli_settings)

    assert isinstance(settings, Settings)
    assert settings.tftp_port == 1969


@mock.patch.dict(os.environ, {"COBBLER_TFTP__TFTP__ADDRESS": "1.2.3.4"})
def test_build_settings_with_env_vars(settings_factory: SettingsFactory):
    settings = settings_factory.build_settings(None)

    assert isinstance(settings, Settings)
    assert settings.tftp_addr == "1.2.3.4"


@mock.patch.dict(os.environ, {"COBBLER_TFTP__TFTP__PORT": "1969"})
def test_build_settings_with_integer_env_vars(settings_factory: SettingsFactory):
    settings = settings_factory.build_settings(None)

    assert isinstance(settings, Settings)
    assert settings.tftp_port == 1969
