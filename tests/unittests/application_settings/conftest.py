"""
This module implements all necessary fixtures for running the unittests using pytests. They are automaticall discovered.
"""

import importlib.resources as importlib_resources
from pathlib import Path

import pytest

from cobbler_tftp.types import SettingsDict


@pytest.fixture
def fake_settings_dict() -> SettingsDict:
    # Test data
    fake_settings_dict: SettingsDict = {
        "schema": 1.0,
        "auto_migrate_settings": True,
        "is_daemon": True,
        "pid_file_path": Path("/run/cobbler-tftp.pid"),
        "cobbler": {
            "uri": "http://localhost/cobbler_api",
            "username": "cobbler",
            "password": "cobbler",
        },
        "tftp": {
            "addr": "127.0.0.1",
            "port": 69,
            "timeout": 2,
            "retries": 5,
        },
        "logging_conf": "/etc/cobbler-tftp/logging.conf",
    }
    return fake_settings_dict


@pytest.fixture
def settings_path() -> Path:
    with importlib_resources.as_file(
        importlib_resources.files("src.cobbler_tftp.settings.data").joinpath(
            "settings.yml"
        )
    ) as settings_path:
        return settings_path
