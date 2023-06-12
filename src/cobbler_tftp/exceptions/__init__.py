"""Custom exceptions for cobbler-tftp."""


class CobblerTftpException(Exception):
    """Generic cobbler-tftp exception."""

    def __init__(self, message: str = "CobblerTFTPException"):
        """Create custom generic CobblerTFTPException."""
        super().__init__(message)
