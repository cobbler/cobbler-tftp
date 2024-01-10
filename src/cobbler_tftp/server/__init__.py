"""
This package contains the actual TFTP server.
"""

import logging
import logging.config

from cobbler_tftp.server.tftp import TFTPServer
from cobbler_tftp.settings import Settings

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files


def run_server(application_settings: Settings):
    """Set up logging, initialize the server and run it."""

    logging_conf = application_settings.logging_conf
    if logging_conf is None or not logging_conf.exists():
        logging_conf = files("cobbler_tftp.settings.data").joinpath("logging.conf")
    logging.config.fileConfig(str(logging_conf))
    logging.debug("Server starting...")
    try:
        address = application_settings.tftp_addr
        port = application_settings.tftp_port
        retries = application_settings.tftp_retries
        timeout = application_settings.tftp_timeout
        server = TFTPServer(address, port, retries, timeout)
    except:  # pylint: disable=bare-except
        logging.exception("Fatal exception while setting up server")
        return
    try:
        server.run()
    except:  # pylint: disable=bare-except
        logging.exception("Fatal exception in server")
    # fbtftp doesn't clean up after exceptions, so we do it here ourselves
    server._metrics_timer.cancel()  # type: ignore
