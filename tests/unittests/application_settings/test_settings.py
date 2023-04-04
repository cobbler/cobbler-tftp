"""
Tests for the application settings module.
"""

from pathlib import Path

import pytest

from cobbler_tftp.settings import Settings, SettingsFactory


@pytest.fixture
def settings_factory():
    """
    Fixture that represends the SettingsFactory class
    """
    return SettingsFactory()


def test_build_settings_with_default_config_file(
    settings_factory: SettingsFactory, mocker
):
    """
    Test the ``build_settings`` function without passing a config file path or additional arguments.

    :assert: True if build successfull and the values of the Settings object correspond to the values inside the default
             config file
    """
    # Call the build_settings method with None as the config_path argument
    settings = settings_factory.build_settings(None, None)

    # Assert that the expected values are set in the Settings object
    assert isinstance(settings, Settings)
    assert settings.auto_migrate_settings is False
    assert settings.is_daemon is True
    assert settings.uri == "http://localhost/cobbler_api"
    assert settings.user == "cobbler"
    assert settings.password == "cobbler"


def test_build_settings_with_valid_config_file(
    settings_factory: SettingsFactory, mocker
):
    valid_file_path = Path("tests/test_data/valid_config.yml")
    settings = settings_factory.build_settings(valid_file_path, None)

    assert isinstance(settings, Settings)
    assert settings.auto_migrate_settings is True
    assert settings.is_daemon is False
    assert settings.uri == "http://testmachine.testnetwork.com/api"
    assert settings.user == "cobbler"
    assert settings.password == "password"


def test_build_settings_with_invalid_config_file(
    settings_factory: SettingsFactory, mocker
):
    # Pass path to invalid yaml file in /test_data/invalid_config.yml
    # Assert that YAMLError gets raised
    path = Path("tests/test_data/invalid_config.yml")

    with pytest.raises(ValueError) as exc:
        settings_factory.build_settings(path, None)

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
    settings = settings_factory.build_settings(path, None)

    # Assert
    captured_message = capsys.readouterr()
    assert captured_message.out == expected_message
    assert isinstance(settings, Settings)
    assert settings.auto_migrate_settings is False
    assert settings.is_daemon is True
    assert settings.uri == "http://localhost/cobbler_api"
    assert settings.user == "cobbler"
    assert settings.password == "cobbler"
