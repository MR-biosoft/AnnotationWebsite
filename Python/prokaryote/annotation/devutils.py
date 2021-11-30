""" Development utility functions """
import os
from typing import Any
from django.core.exceptions import ImproperlyConfigured


def get_env_value(env_variable: str) -> Any:
    """Get credentials, secret keys, passwords, etc.
    From environment variables, raising a descriptive
    error message if they are not set.
    """
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = f"Set the {env_variable} environment variable"
        raise ImproperlyConfigured(error_msg) from None
