""" Development utility functions """
import os
from typing import Any
from pathlib import Path
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


# def _remove_all_filename_extensions(file: Path) -> str:
#    """Remove one or more filename
#    extensions from a pathlib.Path object"""
#    if not isinstance(file, Path):
#        raise TypeError(
#            f"param 'file' expected to be `pathlib.Path`, got {type(file)} instead"
#        )
#    extensions = "".join(file.suffixes)
#    return str(file).replace(extensions, "")
#
#
# def _replace_filename_extension(file: Path, new_extension: str) -> str:
#    """Remove all filename extensions and append `new_extension`"""
#    if new_extension.startswith("."):
#        new_extension = new_extension[1:]
#    return _remove_all_filename_extensions(file) + f".{new_extension}"
