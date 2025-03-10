"""
Schemas for cobbler-tftp settings for validating the parsed settings.

The name of the migration contains the target version.
One migration should be able to update from version x to version x+1, where x is any cobbler-tftp version.
The validation logic of the current version is located in the version's migration file.
"""

import re
import sys
from importlib import import_module
from inspect import signature
from pathlib import Path
from types import ModuleType
from typing import Dict, List

from schema import Schema  # type: ignore[reportMissingTypeStubs]

from cobbler_tftp.exceptions.settings_exceptions import (
    CobblerTftpMissingConfigParameterException,
)
from cobbler_tftp.types import SettingsDict

try:
    import importlib.resources as importlib_resources
except ImportError:
    import importlib_resources  # type: ignore[reportMissingTypeStubs]


class CobblerTftpSchemaVersion:
    """Specifies the version of cobbler-tftp."""

    def __init__(self, major: int = 0, minor: int = 0) -> None:
        """Construct a CobblerTFTPVersion object."""
        self.major = int(major)
        self.minor = int(minor)

    def __eq__(self, other: object) -> bool:
        """Compare two cobbler-tftp version objects."""
        if not isinstance(other, CobblerTftpSchemaVersion):
            return False
        return self.major == other.major and self.minor == other.minor

    def __ne__(self, other: object) -> bool:
        """Compare if two cobbler-tftp version objects are not equal."""
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        """Compare if the current cobbler-tftp version object is less that another."""
        if not isinstance(other, CobblerTftpSchemaVersion):
            raise TypeError
        if self.major < other.major:
            return True
        if self.major.__eq__(other.major):
            if self.minor < other.minor:
                return True
            if self.minor.__eq__(other.minor):
                return True
        return False

    def __le__(self, other: object) -> bool:
        """Compare if current CobblerTFTPVersion object is less or equal another."""
        if self.__lt__(other) or self.__eq__(other):
            return True
        return False

    def __gt__(self, other: object) -> bool:
        """Compare if current CobblerTFTPVersion object is greater than another."""
        if not isinstance(other, CobblerTftpSchemaVersion):
            raise TypeError
        if self.major > other.major:
            return True
        if self.major.__eq__(other.major):
            if self.minor > other.minor:
                return True
            if self.minor.__eq__(other.minor):
                return False
        return False

    def __ge__(self, other: object) -> bool:
        """Compare if current CobblerTFTPVersion object is greater or equal to another."""
        if self.__gt__(other) or self.__eq__(other):
            return True
        return False

    def __hash__(self) -> int:
        """
        Create hash from settings version.

        :return: Hash of settings major and minor version.
        :rtype: hash
        """
        return hash((self.major, self.minor))

    def __str__(self) -> str:
        """
        Return a string representation of the Cobbler-TFTP-Settings object.

        :return: A string containing the version number of the Cobbler-TFTP-Settings object.
        :rtype: str
        """
        return f"Cobbler-TFTP-Settings version: {self.major}.{self.minor}"

    def __repr__(self) -> str:
        """
        Represent the version of the cobbler-tftp settings on the terminal.

        :return: cobbler-tftp settings version as string
        :rtype: str
        """
        return f"CobblerTFTPVersion(major={self.major}, minor={self.minor})"


EMPTY_VERSION: CobblerTftpSchemaVersion = CobblerTftpSchemaVersion()
VERSION_LIST: Dict[CobblerTftpSchemaVersion, ModuleType] = {}
_CONFIG_FILE_PATH: Path = Path()

with importlib_resources.path(__package__, "versioning.cfg") as config_path:  # type: ignore
    _CONFIG_FILE_PATH = config_path  # type: ignore


def __validate_module(name: ModuleType) -> bool:
    """
    Validate if the module is valid and return a boolean result.

    Validate a given module according to two criteria:
        * module must have certain methods implemented
        * methods mut have a certain signature

    :param name: the name of the module to validate
    :return: True if every criteria is met otherwise False
    """
    # noqa for these lines because we can't use the custom types to check this.
    # pylint: disable=line-too-long
    if sys.version_info[:2] >= (3, 13):
        # Starting with Python 3.13 it appears that the real internal path is exposed
        module_methods = {
            "validate": "(settings_dict:Dict[str,Union[float,bool,str,pathlib._local.Path,Dict[str,Union[int,str,pathlib._local.Path]]]])->bool",  # noqa
            "normalize": "(settings_dict:Dict[str,Union[float,bool,str,pathlib._local.Path,Dict[str,Union[int,str,pathlib._local.Path]]]])->Dict[str,Union[float,bool,str,pathlib._local.Path,Dict[str,Union[int,str,pathlib._local.Path]]]]",  # noqa
            "migrate": "(settings_dict:Dict[str,Union[float,bool,str,pathlib._local.Path,Dict[str,Union[int,str,pathlib._local.Path]]]])->Dict[str,Union[float,bool,str,pathlib._local.Path,Dict[str,Union[int,str,pathlib._local.Path]]]]",  # noqa
        }
    else:
        module_methods = {
            "validate": "(settings_dict:Dict[str,Union[float,bool,str,pathlib.Path,Dict[str,Union[int,str,pathlib.Path]]]])->bool",  # noqa
            "normalize": "(settings_dict:Dict[str,Union[float,bool,str,pathlib.Path,Dict[str,Union[int,str,pathlib.Path]]]])->Dict[str,Union[float,bool,str,pathlib.Path,Dict[str,Union[int,str,pathlib.Path]]]]",  # noqa
            "migrate": "(settings_dict:Dict[str,Union[float,bool,str,pathlib.Path,Dict[str,Union[int,str,pathlib.Path]]]])->Dict[str,Union[float,bool,str,pathlib.Path,Dict[str,Union[int,str,pathlib.Path]]]]",  # noqa
        }
    # pylint: enable=line-too-long

    for key, value in module_methods.items():
        if not hasattr(name, key):
            return False
        sig = str(signature(getattr(name, key))).replace(" ", "")
        print(value)
        print(sig)
        if value != sig:
            return False
    return True


def __load_migration_modules(name: str, version: List[str]) -> None:
    """
    Load migration specific modules and if valid adds it to ``VERSION_LIST``.

    :param name: The name of the module to load
    :param version: The migration version as list
    """
    module = import_module(f"cobbler_tftp.settings.migrations.{name}")
    if __validate_module(module):
        version_list_int = [int(i) for i in version]
        VERSION_LIST[CobblerTftpSchemaVersion(*version_list_int)] = module
    else:
        raise RuntimeError(
            f"An Error occured when loading migrations module '{name}' - Module could not be validated."
        )


def get_schema_version(settings_dict: SettingsDict) -> CobblerTftpSchemaVersion:
    """
    Retrieve current cobbler-tftp settings schema version from the settings dict.

    :param settings_dict: The dictionary of settings parameters
    """
    schema_version: list[str] = []
    try:
        schema_version = str(settings_dict.get("schema")).split(".")
    except KeyError as key_error:
        raise CobblerTftpMissingConfigParameterException(
            parameter="schema"
        ) from key_error
    return CobblerTftpSchemaVersion(int(schema_version[0]), int(schema_version[1]))


def discover_migrations() -> None:
    """
    Discovers all available migrations and loads valid ones.

    Discovers the migration module for each cobbler-tftp version and loads it if it is valid according to certain
    conditions:
        * the module must contain the following methods: ``validate()``, ``normalize()``, ``migrate()``
        * those version must have a certain signature
    """
    # importlib.resources.contents is deprecated with 3.11 but files().iterdir() is not yet available in 3.7
    folder_iterator = importlib_resources.contents("cobbler_tftp.settings.migrations")  # type: ignore
    filename_regex = r"v[0-9]*_[0-9]*.py"
    for files in folder_iterator:  # type: ignore
        if not re.match(filename_regex, files):  # type: ignore
            continue
        files = Path(files)  # type: ignore
        if files.is_symlink():
            continue
        migration_name = ""
        if files.suffix == ".py":
            migration_name = files.name[:-3]
        # migration_name should now be something like v3_0
        # Remove leading V. Necessary to save values into CobblerVersion object
        version = migration_name[1:].split("_")
        __load_migration_modules(migration_name, version)


def get_schema(version: CobblerTftpSchemaVersion) -> Schema:
    """
    Return a schema for a given cobbler-tftp version.

    :param version: The cobbler-tftp version object
    :return: The schema of the cobbler-tftp version
    """
    # Unable to use custom protocol from 3.8+ instead of ModuleType
    return VERSION_LIST[version].settings_schema  # type: ignore


def get_current_schema_version() -> CobblerTftpSchemaVersion:
    """
    Get the highest available schema version.

    :return: The highest :class:`CobblerTftpSchemaVersion`.
    """
    highest_version = EMPTY_VERSION
    for version in VERSION_LIST:
        if version > highest_version:
            highest_version = version
    return highest_version


def migrate(
    settings_dict: SettingsDict,
    settings_path: Path,
    old: CobblerTftpSchemaVersion = EMPTY_VERSION,
    new: CobblerTftpSchemaVersion = EMPTY_VERSION,
) -> SettingsDict:
    """
    Migrate to a specific version. If no old and new version is supplied it will call :func:`.auto_migrate`.

    :param settings_dict: The dict of settings parameters to migrate
    :param settings_path: The path of the settings dict
    :param old: The version to migrate from, defaults to :const:`EMPTY_VERSION`
    :param new: The version to migrate to, defaults to :const:`EMPTY_VERSION`
    :raises ValueError: Raised if attempting to downgrade
    :return: The migrated dict
    """
    data: SettingsDict = settings_dict

    if old == EMPTY_VERSION and new == EMPTY_VERSION:
        return auto_migrate(settings_dict, settings_path)

    if EMPTY_VERSION in (old, new):
        raise ValueError("Either both or no versions must be specified to migrate!")

    if old > new:
        raise ValueError("Downgrades are not supported!")

    if old == new:
        return settings_dict

    sorted_version_list = sorted(list(VERSION_LIST.keys()))
    migration_list = sorted_version_list[
        sorted_version_list.index(old) + 1 : sorted_version_list.index(new) + 1
    ]

    for key in migration_list:
        data = VERSION_LIST[key].migrate(settings_dict)

    return data


def auto_migrate(
    settings_dict: SettingsDict,
    settings_path: Path,
) -> SettingsDict:
    """
    Auto migration to the most recent version.

    :param settings_dict: The dictionary of configuration parameters
    :param settings_path: the path of the migration
    :return: The migrated settings as dict
    """

    if not settings_dict.get("auto_migrate_settings", True):
        raise RuntimeError(
            "Automatic migration of settings disabled, but required to run daemon!"
        )
    settings_schema = settings_dict.get("schema", None)
    if settings_schema is None:
        settings_version = get_current_schema_version()
    else:
        if isinstance(settings_schema, float):
            settings_schema_tuple = (
                int(str(settings_schema).split(".", 1)[0]),
                int(str(settings_schema).split(".", 1)[1]),
            )
            settings_version = CobblerTftpSchemaVersion(
                settings_schema_tuple[0], settings_schema_tuple[1]
            )
        else:
            raise ValueError("Invalid Schema version number!")
    if settings_version == EMPTY_VERSION:
        raise RuntimeError(
            "Automigration of settings failed! Settings schema undiscoverable!"
        )

    sorted_version_list = sorted(list(VERSION_LIST.keys()))  # type: ignore
    migrations = sorted_version_list[sorted_version_list.index(settings_version) :]

    for index in range(0, len(migrations) - 1):
        if index == len(migrations) - 1:
            break
        settings_dict = migrate(settings_dict, settings_path)

    return settings_dict


def validate(
    settings_dict: SettingsDict,
) -> bool:
    """
    Tail-call for the methods of the individual migration modules.

    :param settings_dict: The settings dict to validate.
    :return: True if settings are valid, otherwise False.
    """
    version = get_current_schema_version()

    # Extra keys are excluded from validation
    result: bool = VERSION_LIST[version].validate(settings_dict)
    return result


def normalize(
    settings_dict: SettingsDict,
) -> SettingsDict:
    """
    If data in ``settings_dict`` is valid the normalized data is returned.

    :param settings_dict: The settings dict to validate
    :return: The validated dict
    """
    version = get_schema_version(settings_dict)

    result: SettingsDict = VERSION_LIST[version].normalize(settings_dict)

    return result


discover_migrations()
