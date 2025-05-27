"""
This package contains the actual TFTP server.
"""

import logging
import logging.config
from importlib.resources import files

from cobbler_tftp.server.tftp import TFTPServer
from cobbler_tftp.settings import Settings


def run_server(application_settings: Settings):
    """Set up logging, initialize the server and run it."""

    logging_conf = application_settings.logging_conf
    if logging_conf is None or not logging_conf.exists():
        logging_conf = files("cobbler_tftp.settings.data").joinpath("logging.conf")  # type: ignore
    logging.config.fileConfig(str(logging_conf))  # type: ignore
    logging.debug("Server starting...")
    try:
        server = TFTPServer(application_settings)
    except:  # pylint: disable=bare-except
        logging.exception("Fatal exception while setting up server")
        return
    try:
        server.run()
    except:  # pylint: disable=bare-except
        logging.exception("Fatal exception in server")
    server.cleanup()
