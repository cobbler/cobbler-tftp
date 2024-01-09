"""
This module contains the main TFTP server class.
"""

import logging

from fbtftp import BaseHandler, BaseServer, ResponseData


class CobblerResponseData(ResponseData):
    """File-like object representing the response from the TFTP server."""

    def __init__(self):
        pass

    def read(self, n):
        return b""

    def size(self):
        return 0

    def close(self):
        pass


def handler_stats_cb(stats):
    duration = stats.duration() * 1000
    logging.info(
        "Spent %fms processing request for %r from %r",
        duration,
        stats.file_path,
        stats.peer,
    )
    logging.info(
        "Error: %r, sent %d bytes with %d retransmits",
        stats.error,
        stats.bytes_sent,
        stats.retransmits,
    )


def server_stats_cb(stats):
    """
    Called by the fbtftp to log server stats. Currently unused.
    """


class CobblerRequestHandler(BaseHandler):
    """
    Handles TFTP requests using the Cobbler API.
    """

    def __init__(self, server_addr, peer, path, options):
        """
        Initialize a handler for a specific request.

        :param server_addr: Tuple containing the server address and port.
        :param peer: Tuple containing the client address and port.
        :param path: Request file path.
        :param options: Options requested by the client.
        """
        # Future arguments can be handled here
        super().__init__(server_addr, peer, path, options, handler_stats_cb)

    def get_response_data(self):
        return CobblerResponseData()


class TFTPServer(BaseServer):
    """
    Implements a TFTP server for the Cobbler API using the CobblerRequestHandler.
    """

    def __init__(self, address, port, retries, timeout):
        """
        Initialize the TFTP server.

        :param address: IP address to listen on.
        :param port: UDP Port to listen on.
        :param retries: Maximum number of retries when sending a packet fails.
        :param timeout: Timeout for sending packets.
        """
        # Future arguments can be handled here
        self.handler_stats_cb = handler_stats_cb
        super().__init__(address, port, retries, timeout, server_stats_cb)

    def get_handler(self, server_addr, peer, path, options):
        return CobblerRequestHandler(server_addr, peer, path, options)
