"""Build an object containing all cobbler-tftp configuration parameters."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml

from cobbler_tftp.settings import migrations
from cobbler_tftp.types import SettingsDict

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # type: ignore


class Settings:
    """
    Represents the application settings.

    By default, these are read from the default ``settings.yml`` file that is embedded into the application.
    """

    def __init__(
        self,
        auto_migrate_settings: bool,
        is_daemon: bool,
        uri: str,
        username: str,
        password: Union[str, None],
        password_file: Union[Path, None],
    ) -> None:
        """
        Initialize a new instance of the Settings.

        :param auto_migrate_settings: Enable/Disable automatic migration of application settings.
        :param is_daemon: Enable/Disable running cobbler-tftp as daemon.
        :param uri: URI of the cobbler server.
        :param username: Username to authenticate at Cobbler's API.
        :param password: Password for authentication with Cobbler.
        :param password_file: Path to the file containing the password.
        """
        # pylint: disable=R0913

        self.auto_migrate_settings: bool = auto_migrate_settings
        self.is_daemon: bool = is_daemon
        self.uri: str = uri
        self.user: str = username
        self.__password: Union[str, None] = password
        self.__password_file: Union[Path, None] = password_file

    def __repr__(self):
        """
        Print current cobbler-tftp settings to the terminal.

        :return: A string representation of the Settings object.
        :rtype: str
        """

        return f"""
        Cobbler-tftp Application Settings:
        ----------------------------------\n
        Settings auto migration: {self.auto_migrate_settings}\n
        Runs as daemon: {self.is_daemon}

        Connection Settings:
        --------------------\n
        URI: {self.uri}\n
        Username: {self.user}\n
        """

    @property
    def password(self) -> str:
        """
        Get the password from the password file.

        :return: Password string
        """

        if self.__password_file is not None:
            return self.__password_file.read_text()
        if self.__password is not None:
            return self.__password
        return ""


class SettingsFactory:
    """Factory to make it easy building a settings object."""

    def __init__(self) -> None:
        """Initialize a new Settings dicitionary."""
        self._settings_dict: SettingsDict = {}

    def build_settings(
        self, config_path: Optional[Path], cli_arguments: List[str]
    ) -> Settings:
        """
        Build new Settings object using parameters from all sources.

        :param config_path: Path to the configuration file
        :param cli_arguments: List of all CLI configuration options
        :return: Settings object
        """

        # Load config file
        self.load_config_file(config_path)

        # Load environment variables
        self.load_env_variables()

        # Load CLI options
        self.load_cli_options(cli_arguments)

        if not migrations.validate(self._settings_dict):
            raise ValueError(
                """Validation Error: Configuration Parameters could not be validated!\n
                This may be due to an invalid configuration file or path."""
            )

        # Extract parameters from _settings_dict and pass them to the Settings object.
        # Type ignores are necessary as at this point it is not known what value comes from that key.
        auto_migrate_settings: bool = self._settings_dict.get("auto_migrate_settings", False)  # type: ignore
        is_daemon: bool = self._settings_dict.get("is_daemon", False)  # type: ignore
        cobbler_settings = self._settings_dict.get("cobbler", None)
        uri: str = cobbler_settings.get("uri", "")  # type: ignore
        username: str = cobbler_settings.get("username", "")  # type: ignore
        password: str = cobbler_settings.get("password", "")  # type: ignore
        if cobbler_settings.get("password_file", None) is not None:  # type: ignore
            password_file: Optional[Path] = Path(cobbler_settings.get("password_file", None))  # type: ignore
        else:
            password_file = None

        # Create and return a new Settings object
        settings = Settings(
            auto_migrate_settings,
            is_daemon,
            uri,
            username,
            password,
            password_file,
        )

        return settings

    def load_config_file(self, config_path: Union[Path, None]) -> SettingsDict:
        """
        Get config file at given path. Load contents and put into settings dict.

        :param config_path: Path to configuration file. Can be either customized via CLI or default if none
        :return _settings_dict: Dictionary containing all settings from the settings.yml file
        """

        config_file = str(config_path).rsplit("/", maxsplit=1)[-1]
        config_pure_path = Path(str(config_path).replace(config_file, ""))
        config_import_path = str(config_pure_path).replace("/", ".", -1)

        if not config_path or config_path == "" or not Path.exists(config_path):
            if config_path and not Path.exists(config_path):  # type: ignore
                # Prompt the user that no configuration file could be found and the default will be used
                print(
                    f"Warning: No configuration file found at {config_path}! Using default configuration file..."
                )
            try:
                config_file_content = (
                    files("cobbler_tftp.settings.data")
                    .joinpath("settings.yml")
                    .read_text(encoding="UTF-8")
                )
                self._settings_dict = yaml.safe_load(config_file_content)
            except yaml.YAMLError:
                print(f"Error: No valid configuration file found at {config_path}!")
        elif config_path and Path.exists(config_path):
            try:
                config_file_content = (
                    files(config_import_path).joinpath(config_file).read_text("utf-8")
                )
                self._settings_dict = yaml.safe_load(config_file_content)
            except yaml.YAMLError:
                print(f"Error: No valid configuration file found at {config_path}!")
        return self._settings_dict

    def load_env_variables(self) -> SettingsDict:
        """
        Get environment variables containing relevant settings.

        These will override keys taken from the ``settings.yml`` file if applicable.
        """

        cobbler_keys = [x for x in os.environ if x.startswith("COBBLER_TFTP__")]

        # return the settings dictionary if no environment variables exist
        if len(cobbler_keys) == 0:
            return self._settings_dict

        for variable in cobbler_keys:
            key_path = variable.split("__")
            key_to_update = key_path[-1]

            if len(key_path) == 2:
                try:
                    self._settings_dict.update(
                        {key_to_update.lower(): str(os.environ[variable])}
                    )
                except KeyError as exc:
                    print(exc)
            else:
                setting_to_update = {key_to_update.lower(): str(os.environ[variable])}

                for pos in range(len(key_path) - 2, 1, -1):
                    setting_to_update = {key_path[pos]: setting_to_update}

                self._settings_dict.update(setting_to_update)  # type: ignore

                return self._settings_dict
        return self._settings_dict

    def load_cli_options(
        self,
        daemon: Optional[bool] = None,
        enable_automigration: Optional[bool] = None,
        settings: Optional[Dict[str, Union[str, Path]]] = None,
    ) -> SettingsDict:
        """
        Get parameters and flags from CLI.

        These will override the ones taken from the settings file or environment variables and are meant for
        controlling parameters of the application temporarily.

        :param daemon: If the application should be run in the background as a daemon or not.
        :param enable_automigration: Whether to enable the automigration or not.
        :param settings: List of custom settings which can be entered manually.
                         Each entry has the format: ``<PARENT_YAML_KEY>.<CHILD_YAML_KEY>.<...>.<KEY_NAME>=<VALUE>``
        :return _settings_dict: Settings dictionary.
        """

        if not daemon and not enable_automigration and not settings:
            return self._settings_dict

        if daemon:
            self._settings_dict["is_daemon"] = daemon
        if enable_automigration:
            self._settings_dict["auto_migrate_settings"] = enable_automigration

        if settings is None:
            raise ValueError
        for setting in settings:
            option_list = setting.split("=", 1)

            if "." not in option_list[0]:
                self._settings_dict.update({option_list[0]: option_list[1]})
            else:
                parent = option_list[0].split(".")

                setting_to_update = {parent[-1]: option_list[1]}

                for key in range(len(parent), 0, -1):
                    setting_to_update = {parent[key]: setting_to_update}

                self._settings_dict.update(setting_to_update)  # type: ignore

                return self._settings_dict
        return self._settings_dict
