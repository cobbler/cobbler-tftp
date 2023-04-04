"""Whitelist for vulture to ignore certain methods as unused."""

import cobbler_tftp.settings.migrations.v1_0 as migration

migration.migrate({})
migration.normalize({})
migration.validate({})
