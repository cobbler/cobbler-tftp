"""
Cobbler-tftp will be managable as a command-line service.
"""

import os
from pathlib import Path
from signal import SIGTERM
from typing import List, Optional

import click
import yaml
from daemon import DaemonContext

try:
    import importlib.metadata as importlib_metadata
except ImportError:  # use backport for Python versions older than 3.8
    import importlib_metadata

from cobbler_tftp.server import run_server
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
    The value is parsed as YAML. Quotes around the value are recommended for strings.""",
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
    if config is None:
        config_path = None
    else:
        config_path = Path(config)
    application_settings = SettingsFactory().build_settings(
        config_path, daemon, enable_automigration, settings
    )
    if application_settings.is_daemon:
        click.echo("Starting daemon...")
        with DaemonContext():
            # All previously open file descriptors are invalid now.
            # Files and connections needed for the daemon should be opened
            # in run_server or listed in the files_preserve option
            # of DaemonContext.

            application_settings.pid_file_path.write_text(str(os.getpid()))
            try:
                run_server(application_settings)
            finally:
                application_settings.pid_file_path.unlink()
    else:
        click.echo("Daemon mode disabled, running in foreground.")
        run_server(application_settings)


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
    click.echo(SettingsFactory().build_settings(None))


@cli.command()
@click.option(
    "--config", "-c", type=click.Path(), help="Set location of configuration file."
)
@click.option("--pid-file", "-p", type=click.Path(), help="Set location of PID file.")
def stop(config: Optional[str], pid_file: Optional[str]):
    """
    Stop the cobbler-tftp server daemon if it is running
    """
    if pid_file is None:
        if config is None:
            config_path = None
        else:
            config_path = Path(config)
        application_settings = SettingsFactory().build_settings(config_path)
        pid_file_path = application_settings.pid_file_path
    else:
        pid_file_path = Path(pid_file)
    try:
        pid = int(pid_file_path.read_text(encoding="UTF-8"))
    except OSError:
        click.echo("Unable to read PID file. The daemon is probably not running.")
        return
    try:
        os.kill(pid, SIGTERM)
    except ProcessLookupError:
        click.echo("Stale PID file. The daemon is no longer running.")
    pid_file_path.unlink()


cli.add_command(start)
cli.add_command(version)
cli.add_command(print_default_config)
cli.add_command(stop)
