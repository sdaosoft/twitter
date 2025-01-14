from utils import sleep
from .session import BaseAsyncSession

from typing import TypeVar
from tenacity import retry, stop_after_attempt, wait_fixed

T = TypeVar("T", bound="BaseHTTPClient")


class BaseHTTPClient:
    _DEFAULT_HEADERS = None

    def __init__(self, **session_kwargs):
        self._session = BaseAsyncSession(
            verify=False,
            trust_env=True,
            headers=session_kwargs.pop("headers", None) or self._DEFAULT_HEADERS,
            **session_kwargs,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        await self._session.close()

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1), reraise=True)
    async def request_session(self, method, url, **kwargs):
        return await self._session.request(method, url, **kwargs)
