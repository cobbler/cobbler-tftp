"""Custom exceptions for cobbler-tftp's settings module."""


class CobblerTftpSettingsException(Exception):
    """Generic cobbler-tftp exception."""

    def __init__(self, message: str = "An Error occured!"):
        """Create custom generic settings exception."""
        super().__init__(message)


class CobblerTftpMissingConfigParameterException(KeyError):
    """Exception to handle a missing but required config parameter."""

    def __init__(
        self,
        message="MissingConfigParameterException: Application settings missing required parameter!",
        parameter: str = "NONE",
    ):
        """Create custom exception to raise when a specific config parameter is missing for the application settings."""
        if parameter is None or parameter == "NONE":
            raise ValueError("Parameter cannot be 'NONE'")
        self.parameter = parameter
        self.message = str.join(message, parameter)
        super().__init__(message, parameter)
