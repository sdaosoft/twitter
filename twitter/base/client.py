from .session import BaseAsyncSession

from typing import Callable, TypeVar, Any
from functools import wraps
from curl_cffi.requests.errors import RequestsError

T = TypeVar("T", bound="BaseHTTPClient")


def retry(
        retry_times: int = 1,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[[T, Any], Any]) -> Callable[[T, Any], Any]:
        @wraps(func)
        async def wrapper(self: "BaseHTTPClient", *args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(retry_times + 1):
                try:
                    return await func(self, *args, **kwargs)
                except RequestsError as e:
                    last_exception = e

            raise last_exception

        return wrapper

    return decorator


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

    @retry(retry_times=2)
    async def request_session(self, method, url, **kwargs):
        return await self._session.request(method, url, **kwargs)
