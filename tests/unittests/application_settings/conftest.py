"""
This module implements all necessary fixtures for running the unittests using pytests. They are automaticall discovered.
"""
import pytest

from cobbler_tftp.types import SettingsDict

try:
    import importlib.resources as importlib_resources
except ImportError:
    import importlib_resources as importlib_resources  # type: ignore


@pytest.fixture
def fake_settings_dict() -> SettingsDict:
    # Test data
    fake_settings_dict: SettingsDict = {
        "schema": 1.0,
        "auto_migrate_settings": True,
        "is_daemon": True,
        "cobbler": {
            "uri": "http://localhost/cobbler_api",
            "username": "cobbler",
            "password": "cobbler",
        },
    }
    return fake_settings_dict


@pytest.fixture
def settings_path():
    with importlib_resources.path(
        "src.cobbler_tftp.settings.data", "settings.yml"
    ) as settings_path:
        return settings_path
