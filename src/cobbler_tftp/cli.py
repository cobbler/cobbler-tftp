"""
Cobbler-tftp will be managable as a command-line service.
"""

from pathlib import Path
from typing import List, Optional

import click
import yaml

try:
    import importlib.metadata as importlib_metadata
except ImportError:  # use backport for Python versions older than 3.8
    import importlib_metadata

from cobbler_tftp.settings import SettingsFactory

try:
    __version__ = importlib_metadata.version("cobbler_tftp")
except importlib_metadata.PackageNotFoundError:
    __version__ = "unknown (not installed)"

_context_settings = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=_context_settings, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    Cobbler-TFTP - Copyright (c) 2022 The Cobbler Team. (github.com/cobbler)\n
    Licensed under the terms of the GPLv2.0 license.
    """
    if ctx.invoked_subcommand is None:
        click.echo(
            "No commands given, try 'cobbler-tftp -h' or 'cobbler-tftp --help' to view usage."
        )

        # Possible default behavior can be invoked here


@cli.command()
@click.option(
    "--daemon/--no-daemon",
    "-d/-dd",
    is_flag=True,
    default=None,
    help="Force cobbler-tftp to run as daemon or not.",
)
@click.option(
    "--enable-automigration/--disable-automigration",
    is_flag=True,
    default=None,
    help="Enable or disable auto migration of settings.",
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
def start(
    daemon: Optional[bool],
    enable_automigration: Optional[bool],
    config: Optional[str],
    settings: List[str],
):
    """
    Start the cobbler-tftp server.
    """
    click.echo(cli.__doc__)
    click.echo("Initializing Cobbler-tftp server...")
    settings_factory: SettingsFactory = SettingsFactory()
    # settings_file = SettingsFactory.load_config_file(settings_factory, config)
    # environment_variables = SettingsFactory.load_env_variables(settings_factory)
    # cli_arguments = SettingsFactory.load_cli_options(
    #     settings_factory, daemon, enable_automigration, settings
    # )
    if config is None:
        config_path = None
    else:
        config_path = Path(config)
    application_settings = SettingsFactory.build_settings(
        settings_factory, config_path, daemon, enable_automigration, settings
    )
    print(application_settings)


@cli.command()
def version():
    """
    Check cobbler-tftp version. If there are any cobbler servers connected their versions will be printed as well.
    """
    click.echo(f"Cobbler-tftp {__version__}")


@cli.command()
def print_default_config():
    """
    Print the default application parameters.
    """
    settings_factory: SettingsFactory = SettingsFactory()
    click.echo(settings_factory.build_settings(None))


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
