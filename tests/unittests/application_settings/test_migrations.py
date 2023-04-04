"""
Tests for the settings schemas in the migrations module.
"""

from pathlib import Path
from typing import List

import pytest
import pytest_mock
from schema import Schema

import cobbler_tftp.settings.migrations as migrations
from cobbler_tftp.types import SettingsDict
from tests.conftest import does_not_raise
from tests.unittests.application_settings.conftest import fake_settings_dict

fake_new_settings_dict: SettingsDict = {
    "schema": 2.0,
    "auto_migrate_settings": True,
    "is_daemon": True,
    "cobbler": {
        "uri": "http://localhost/cobbler_api",
        "username": "cobbler",
        "password": "cobbler",
    },
}


@pytest.fixture(autouse=True)
def reset_version_list():
    # Arrange
    migrations.VERSION_LIST = {}
    # Act
    yield
    # Cleanup
    migrations.discover_migrations()


def test_get_schema_version(fake_settings_dict):
    # Arrange & Act
    schema_version = migrations.get_schema_version(fake_settings_dict)

    # Assert
    assert schema_version.major == 1
    assert schema_version.minor == 0


def test_discover_migrations(mocker: "pytest_mock.MockerFixture"):
    # Arrange
    # Define a list of mock migration module names
    mock_migrations: List[str] = [
        "v1_0.py",
        "v2_0.py",
        "v3_0.py",
        "not_a_migration.py",
        "v4_0.py",
    ]
    # Replace importlib_resources.contents with a mock object that returns the mock contents
    mock_importlib = mocker.patch(
        "cobbler_tftp.settings.migrations.importlib_resources.contents",
        return_value=mock_migrations,
    )
    # Replace __load_migration_modules with a mock object that does nothing
    mock_load_migration = mocker.patch(
        "cobbler_tftp.settings.migrations.__load_migration_modules",
        return_value=None,
    )

    # Act
    migrations.discover_migrations()

    # Assert
    # types will be ignored as assert_has_calls expects unittest.mock instead of mocker calls
    mock_load_migration.assert_has_calls(
        [
            mocker.call("v1_0", ["1", "0"]),  # type: ignore
            mocker.call("v2_0", ["2", "0"]),  # type: ignore
            mocker.call("v3_0", ["3", "0"]),  # type: ignore
            mocker.call("v4_0", ["4", "0"]),  # type: ignore
        ]
    )

    mock_importlib.assert_called_once_with("cobbler_tftp.settings.migrations")


def test_get_schema(mocker: "pytest_mock.MockerFixture"):
    # Arrange
    # Fake schema and version
    version = migrations.CobblerTftpSchemaVersion(1, 0)
    schema = Schema({})
    module_mock = mocker.MagicMock()
    module_mock.settings_schema = schema
    migrations.VERSION_LIST[version] = module_mock

    # Act
    result = migrations.get_schema(version)

    # Assert
    assert result == schema


def test_get_current_schema_version(mocker: "pytest_mock.MockerFixture"):
    # Arrange
    version = migrations.CobblerTftpSchemaVersion(99, 0)
    schema = Schema({})
    module_mock = mocker.MagicMock()
    module_mock.settings_schema = schema
    migrations.VERSION_LIST[version] = module_mock
    migrations.discover_migrations()

    # Act
    result = migrations.get_current_schema_version()

    # Assert
    assert result == version


def test_migrate_without_parameters(mocker):
    # Arrange
    mock_auto_migrate = mocker.patch(
        "cobbler_tftp.settings.migrations.migrate", return_value=SettingsDict
    )

    # Act
    migrations.migrate({}, Path())

    # Assert
    mock_auto_migrate.assert_called_once()


@pytest.mark.parametrize(
    "settings_dict, settings_path, old, new, expected, expected_exception",
    [
        (
            fake_settings_dict,
            Path(),
            migrations.CobblerTftpSchemaVersion(1, 0),
            None,
            None,
            pytest.raises(TypeError),
        ),
        (
            fake_settings_dict,
            Path(),
            migrations.CobblerTftpSchemaVersion(2, 0),
            migrations.CobblerTftpSchemaVersion(1, 0),
            None,
            pytest.raises(ValueError),
        ),
        (
            fake_settings_dict,
            Path(),
            migrations.CobblerTftpSchemaVersion(1, 0),
            migrations.CobblerTftpSchemaVersion(1, 0),
            fake_settings_dict,
            does_not_raise(),
        ),
    ],
)
def test_migrate(settings_dict, settings_path, old, new, expected, expected_exception):
    # Arrange
    if expected is not None and old and new is None:
        expected = expected()
    # Act
    with expected_exception:
        result = migrations.migrate(settings_dict, settings_path, old, new)
        # Assert
        assert result == expected


def test_auto_migrate_calls_migrate(
    mocker: "pytest_mock.MockerFixture", fake_settings_dict, settings_path
):
    # Arrange
    migrations.VERSION_LIST[
        migrations.CobblerTftpSchemaVersion(1, 0)
    ] = mocker.MagicMock()
    migrations.VERSION_LIST[
        migrations.CobblerTftpSchemaVersion(2, 0)
    ] = mocker.MagicMock()
    mock_migrate = mocker.patch("cobbler_tftp.settings.migrations.migrate")

    # Act
    migrations.auto_migrate(fake_settings_dict, settings_path)

    # Assert
    mock_migrate.assert_called_once_with(fake_settings_dict, settings_path)


def test_auto_migrate_raises_runtime_error(fake_settings_dict, settings_path):
    # Arrange
    fake_settings_dict["auto_migrate_settings"] = False

    # Act and Assert
    with pytest.raises(RuntimeError):
        migrations.auto_migrate(fake_settings_dict, settings_path)


def test_auto_migrate_raises_value_error(fake_settings_dict, settings_path):
    # Arrange
    fake_settings_dict["schema"] = "not float"

    # Act and Assert
    with pytest.raises(ValueError):
        migrations.auto_migrate(fake_settings_dict, settings_path)


def test_auto_migrate_raises_value_error_if_verions_empty(
    fake_settings_dict, settings_path
):
    # Arrange
    fake_settings_dict["schema"] = migrations.EMPTY_VERSION

    # Act and Assert
    with pytest.raises(ValueError):
        migrations.auto_migrate(fake_settings_dict, settings_path)


def test_validate(mocker, fake_settings_dict):
    # Arrange
    mock_validation_module = mocker.MagicMock()
    mock_validation_module.validate = mocker.MagicMock(return_value=True)
    version = migrations.CobblerTftpSchemaVersion(1, 0)
    mocker.patch(
        "cobbler_tftp.settings.migrations.get_current_schema_version",
        return_value=version,
    )
    migrations.VERSION_LIST[version] = mock_validation_module

    # Act
    result = migrations.validate(fake_settings_dict)

    # Assert
    mock_validation_module.validate.assert_called_once_with(fake_settings_dict)
    assert result is True


def test_normalize(mocker, fake_settings_dict):
    # Arrange
    mock_validation_module = mocker.MagicMock()
    mock_validation_module.normalize = mocker.MagicMock(return_value=True)
    version = migrations.CobblerTftpSchemaVersion(1, 0)
    mocker.patch(
        "cobbler_tftp.settings.migrations.get_schema_version",
        return_value=version,
    )
    migrations.VERSION_LIST[version] = mock_validation_module

    # Act
    result = migrations.normalize(fake_settings_dict)

    # Assert
    mock_validation_module.normalize.assert_called_once_with(fake_settings_dict)
    assert result is True
