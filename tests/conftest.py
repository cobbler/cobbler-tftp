"""
Fixtures for all tests
"""

from contextlib import contextmanager


@contextmanager
def does_not_raise():
    """
    Fixture that represents a context manager that will expect that no raise occurs.
    """
    yield
