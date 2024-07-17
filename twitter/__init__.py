"""
Twitter API Wrapper
~~~~~~~~~~~~~~~~~~~

A Python library for interacting with the Twitter API.
"""

from .client import Client
from .account import (
    Account,
    AccountStatus,
)
from .models import Tweet, User, Media, Image
from . import errors, utils

__all__ = [
    "Client",
    "Account",
    "AccountStatus",
    "Tweet",
    "User",
    "Media",
    "Image",
    "utils",
    "errors",
]


import warnings

# HACK: Ignore event loop warnings from curl_cffi
warnings.filterwarnings("ignore", module="curl_cffi")

from loguru import logger

logger.disable("twitter")
