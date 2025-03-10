"""
This module contains the main TFTP server class.
"""

import logging
import os
import time
import xmlrpc.client
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from fbtftp import (  # type: ignore[reportMissingTypeStubs]
    BaseHandler,
    BaseServer,
    ResponseData,
    SessionStats,
)
from fbtftp.base_server import ServerStats  # type: ignore[reportMissingTypeStubs]

from cobbler_tftp.settings import Settings


class CobblerResponseData(ResponseData):
    """
    File-like object representing the response from the TFTP server.
    Data is fetched from the API in chunks. These chunks may be larger
    than the TFTP request chunks, so the returned chunks are cached.
    """

    def __init__(
        self, api: xmlrpc.client.Server, token: str, path: str, prefetch_size: int
    ):
        self._api = api
        self._token = token
        self._path = path
        self._size: Optional[int] = None
        self._chunk: Optional[bytes] = None
        self._chunk_offset = 0
        self._file_offset = 0
        self._prefetch_size = prefetch_size

    def load(self) -> None:
        binary: xmlrpc.client.Binary
        binary, self._size = self._api.get_tftp_file(  # type: ignore
            self._path, self._file_offset, self._prefetch_size, self._token
        )
        self._chunk = binary.data

    def read(self, n: int) -> bytes:
        if self._chunk is None:
            raise RuntimeError("load() not called")
        if n > self._prefetch_size:
            raise ValueError("Chunk too large")
        end = self._chunk_offset + n
        if end <= self._prefetch_size:
            data = self._chunk[self._chunk_offset : end]
            self._chunk_offset = end
            return data
        self._file_offset += self._chunk_offset
        self.load()
        data = self._chunk[:n]
        self._chunk_offset = len(data)
        return data

    def size(self) -> int:
        if self._size is None:
            raise RuntimeError("load() not called")
        return self._size

    def close(self):
        pass


class FileResponseData(ResponseData):
    """Object representing a static file response from the TFTP server."""

    def __init__(self, path: Path):
        self._io = open(path, "rb")
        self._size = path.stat().st_size

    def read(self, n: int) -> bytes:
        return self._io.read(n)

    def size(self) -> int:
        return self._size

    def close(self):
        self._io.close()


def handler_stats_cb(stats: SessionStats):
    duration = stats.duration() * 1000
    logging.info(
        "Spent %fms processing request for %r from %r",
        duration,
        stats.file_path,  # type: ignore[reportUnkownArgumentType]
        stats.peer,  # type: ignore[reportUnkownArgumentType]
    )
    logging.info(
        "%r, sent %d bytes with %d retransmits",
        stats.error,  # type: ignore[reportUnkownArgumentType]
        stats.bytes_sent,
        stats.retransmits,
    )


def server_stats_cb(stats: ServerStats):
    """
    Called by the fbtftp to log server stats. Currently unused.
    """


class CobblerRequestHandler(BaseHandler):
    """
    Handles TFTP requests using the Cobbler API.
    """

    def __init__(
        self,
        server_addr: Tuple[str, int],
        peer: Tuple[str, int],
        path: str,
        options: Dict[str, Any],
        api: xmlrpc.client.Server,
        token: str,
        settings: Settings,
    ):
        """
        Initialize a handler for a specific request.

        :param server_addr: Tuple containing the server address and port.
        :param peer: Tuple containing the client address and port.
        :param path: Request file path.
        :param options: Options requested by the client.
        :param api: The Cobbler API object.
        :param token: Login token for accessing the Cobbler API.
        :param settings: The cobbler-tftp application settings.
        """
        self._api = api
        self._token = token
        self._settings = settings
        super().__init__(server_addr, peer, path, options, handler_stats_cb)

    def get_response_data(self):
        resp = CobblerResponseData(
            self._api, self._token, self._path, self._settings.prefetch_size  # type: ignore[reportUnkownArgumentType]
        )
        try:
            resp.load()
            return resp
        except xmlrpc.client.Error as err:
            logging.warning("Could not fetch %s from server: %r", self._path, err)  # type: ignore[reportUnkownArgumentType]
            if self._settings.static_fallback_dir is not None:
                path = os.path.normpath(os.path.join("/", self._path)).strip("/")  # type: ignore[reportUnkownArgumentType]
                return FileResponseData(self._settings.static_fallback_dir / path)
            raise err


class TFTPServer(BaseServer):
    """
    Implements a TFTP server for the Cobbler API using the CobblerRequestHandler.
    """

    def __init__(self, settings: Settings):
        """
        Initialize the TFTP server.

        :param settings: The cobbler-tftp application settings.
        """
        self._token = None
        self._token_renew_time = 0.0
        self._settings = settings
        super().__init__(  # type: ignore[reportUnkownMemberType]
            settings.tftp_addr,
            settings.tftp_port,
            settings.tftp_retries,
            settings.tftp_timeout,
            server_stats_cb,
        )

    def _renew_token(self, api: xmlrpc.client.Server):
        start_time = time.monotonic()
        if start_time >= self._token_renew_time:
            self._token = api.login(self._settings.user, self._settings.password)
            self._token_renew_time = start_time + self._settings.token_refresh_interval

    def cleanup(self):
        if self._token is not None:
            if time.monotonic() < self._token_renew_time:
                xmlrpc.client.Server(self._settings.uri).logout(self._token)
        # fbtftp doesn't clean up after exceptions, so we do it here ourselves
        self._metrics_timer.cancel()  # type: ignore

    def get_handler(
        self,
        server_addr: Tuple[str, int],
        peer: Tuple[str, int],
        path: str,
        options: Dict[str, Any],
    ):
        api = xmlrpc.client.Server(self._settings.uri)
        self._renew_token(api)
        return CobblerRequestHandler(
            server_addr, peer, path, options, api, self._token, self._settings  # type: ignore[reportArgumentType]
        )
