"""Module for the validation, normalization and migration of the schema version "1.0"."""

from pathlib import Path

from schema import (  # type: ignore[reportMissingTypeStubs]
    Optional,
    Or,
    Schema,
    SchemaError,
    SchemaWrongKeyError,
)

from cobbler_tftp.types import SettingsDict

settings_schema: Schema = Schema(
    {
        Optional("schema"): float,
        Optional("auto_migrate_settings"): bool,
        Optional("is_daemon"): bool,
        Optional("pid_file_path"): str,
        Optional("cobbler"): {
            Optional("uri"): str,
            Optional("username"): str,
            # We cannot use only_one since python-schema is only available in 0.6.7 in SLES 15.6
            # Optional(Or("password", "password_file", only_one=True)): Or(str, Path),  # type: ignore[reportArgumentType]
            Optional("password"): Or(str, Path),  # type: ignore[reportArgumentType]
            Optional("password_file"): Or(str, Path),  # type: ignore[reportArgumentType]
            Optional("token_refresh_interval"): int,
        },
        Optional("prefetch_size"): int,
        Optional("tftp"): {
            Optional("address"): str,
            Optional("port"): int,
            Optional("retries"): int,
            Optional("timeout"): int,
            Optional("static_fallback_dir"): str,
        },
        Optional("logging_conf"): str,
    }
)


def validate(settings_dict: SettingsDict) -> bool:
    """
    Validate the given dictionary of configuration parameters to the reference ``schema``.

    :param settings_dict: The dictionary of configuration parameters to validate
    :return bool: True/False depending on whether the dicts match or not
    """
    if settings_dict == {} or settings_dict is None:  # type: ignore[reportUncessaryComparison]
        return False

    try:
        settings_schema.validate(settings_dict)
    except (SchemaError, SchemaWrongKeyError) as exc:
        print(exc)
        return False
    return True


def normalize(settings_dict: SettingsDict) -> SettingsDict:
    """
    If data in ``settings_dict`` is valid, the validated data is returned.

    :param settings_dict: The dictionary of configuration parameters to validate
    :return: the validated dict
    :rtype dict:
    """
    return settings_schema.validate(settings_dict)


def migrate(settings_dict: SettingsDict) -> SettingsDict:
    """
    Migrate settings dict from previous to current version.

    :param settings_dict: The dictionary to migrate
    :return: The settings dict
    """
    if not validate(settings_dict):
        raise SchemaError("v1.0.0: Schema error while validating")
    return normalize(settings_dict)
