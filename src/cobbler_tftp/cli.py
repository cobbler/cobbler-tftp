"""
Cobbler-tftp will be managable as a command-line service.
"""

import click
import yaml

from cobbler_tftp.settings import SettingsFactory

with open("src/cobbler_tftp/settings/data/settings.yml", "r", encoding="utf-8") as stream:
    try:
        SETTINGS = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

_context_settings = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=_context_settings, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    Cobbler-TFTP - Copyright (c) 2022 The Cobbler Team. (github.com/cobbler)\n
    Licensed under the terms of the GPLv2.0 license.
    """
    if ctx.invoked_subcommand is None:
        click.echo("No commands given, try 'cobbler-tftp -h' or 'cobbler-tftp --help' to view usage.")

        # Possible default behavior can be invoked here


@cli.command()
@click.option(
    "--no-daemon",
    "-dd",
    is_flag=True,
    default=SETTINGS["is_daemon"], #type: ignore
    help="Stop cobbler-tftp from running as daemon.",
)
@click.option(
    "--enable-automigration",
    is_flag=True,
    default=SETTINGS["auto_migrate_settings"], #type: ignore
    help="Enable auto migration of settings.",
)
@click.option(
    "--config", "-c", type=click.Path(), help="Set location of configuration file."
)
@click.option(
    "--settings",
    "-s",
    multiple=True,
    help="""Set custom settings in format:\n
    <PARENT_YAML_KEY>.<CHILD_YAML_KEY>.<...>.<KEY_NAME>=<VALUE>.\n
    Your settings must use single quotes. If a single quote appears within a value it must be escaped.""",
)
def start(daemon: bool, enable_automigration, config, settings):
    """
    Start the cobbler-tftp server.
    """
    click.echo(
        f"Cobbler-tftpCopyright (c) 2023\nLicensed under the terms of the GPL-v2.0 license.\nInitializing Cobbler-tftp server...\n"
    )
    if daemon:
        click.echo(
            f"'--daemon' flag set.\nCobbler-tftp will be running as a daemon in the background."
        )
    else:
        click.echo(f"Server running...")
        settings_factory: SettingsFactory = SettingsFactory()
        # settings_file = SettingsFactory.load_config_file(settings_factory, config)
        # environment_variables = SettingsFactory.load_env_variables(settings_factory)
        # cli_arguments = SettingsFactory.load_cli_options(
        #     settings_factory, daemon, enable_automigration, settings
        # )
        application_settings = SettingsFactory.build_settings(
            settings_factory, config, settings
        )


@cli.command()
def version():
    """
    Check cobbler-tftp version. If there are any cobbler servers connected their versions will be printed as well.
    """
    pass


@cli.command()
def print_default_config():
    """
    Print the default application parameters.
    """
    pass


@cli.command()
def stop():
    """
    Stop the cobbler-tftp server daemon if it is running
    """
    pass


cli.add_command(start)
cli.add_command(version)
cli.add_command(print_default_config)
cli.add_command(stop)