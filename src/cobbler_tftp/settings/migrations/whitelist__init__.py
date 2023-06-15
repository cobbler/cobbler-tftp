"""Whitelist for vulture to ignore certain methods as unused."""

from cobbler_tftp.settings.migrations import EMPTY_VERSION, get_schema

# Ignore because we potentially require this later when implementing other features.
get_schema(EMPTY_VERSION)
