"""
Cobbler-tftp will be managable as a command-line service.
"""

import os
import sys
from pathlib import Path
from signal import SIGCHLD, SIGTERM
from typing import List, Optional

import click
from daemon import DaemonContext  # type: ignore

try:
    import importlib.metadata as importlib_metadata
except ImportError:  # use backport for Python versions older than 3.8
    import importlib_metadata  # type: ignore

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # type: ignore

from cobbler_tftp.server import run_server
from cobbler_tftp.settings import SettingsFactory
from cobbler_tftp.utils import copy_file  # type: ignore

try:
    __version__ = importlib_metadata.version("cobbler_tftp")  # type: ignore
except importlib_metadata.PackageNotFoundError:  # type: ignore
    __version__ = "unknown (not installed)"

_context_settings = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=_context_settings, invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context):
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
    "--config",
    "-c",
    default="/etc/cobbler-tftp/settings.yml",
    type=click.Path(),
    help="Set location of configuration file.",
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
        with DaemonContext(signal_map={SIGCHLD: None}):
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


@cli.command()
@click.option(
    "--systemd-dir",
    type=click.Path(),
    default="/etc/systemd/system",
    help="Where to install systemd unit files",
)
@click.option(
    "--config-dir",
    type=click.Path(),
    default="/etc/cobbler-tftp",
    help="Where to install the configuration files for cobbler-tftp",
)
@click.option(
    "--systemd/--no-systemd",
    is_flag=True,
    default=True,
    help="Whether to install systemd unit files or not",
)
@click.option(
    "--install-prefix",
    type=click.Path(),
    default=None,
    help="Installation prefix for the file locations that will be ignored during runtime",
)
def setup(
    systemd_dir: str,
    config_dir: str,
    systemd: bool,
    install_prefix: Optional[str],
):
    """
    Install configuration files and systemd unit files into the specified directories
    """
    if install_prefix is not None:
        systemd_path = Path(install_prefix, systemd_dir.strip("/"))
        config_path = Path(install_prefix, config_dir.strip("/"))
    else:
        systemd_path = Path(systemd_dir)
        config_path = Path(config_dir)
        config_dir = str(config_path.absolute())
    try:
        config_path.mkdir(parents=True, exist_ok=True)
        source_path = files("cobbler_tftp.settings.data")  # type: ignore
        if systemd:
            systemd_path.mkdir(parents=True, exist_ok=True)
            copy_file(source_path, systemd_path, "cobbler-tftp.service")
        copy_file(
            source_path,
            config_path,
            "settings.yml",
            [("/etc/cobbler-tftp", config_dir)],
        )
        copy_file(source_path, config_path, "logging.conf")
    except PermissionError as err:
        click.echo(err, err=True)
        click.echo(
            "Try changing the --systemd-dir/--config-dir parameters or running as root."
        )
        sys.exit(1)


cli.add_command(start)
cli.add_command(version)
cli.add_command(print_default_config)
cli.add_command(stop)
cli.add_command(setup)
