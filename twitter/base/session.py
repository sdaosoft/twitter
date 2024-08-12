from __future__ import annotations

from curl_cffi import requests
from better_proxy import Proxy


class BaseAsyncSession(requests.AsyncSession):
    """
    Базовая асинхронная сессия:
        - Принимает прокси в формате URL и better-proxy.
        - По умолчанию устанавливает версию браузера chrome120.
        - По умолчанию устанавливает user-agent под версию браузера chrome120.
    """

    proxy: Proxy | None
    DEFAULT_HEADERS = {
        "accept": "*/*",
        "accept-language": "en-US,en",
        "Priority": "u=1, i",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "ssame-site",
        "connection": "keep-alive",
    }
    DEFAULT_IMPERSONATE = requests.BrowserType.chrome124

    def __init__(
        self,
        proxy: str | Proxy = None,
        **session_kwargs,
    ):
        self._proxy = None
        headers = session_kwargs["headers"] = session_kwargs.get("headers") or {}
        headers.update(self.DEFAULT_HEADERS)
        session_kwargs["impersonate"] = (
            session_kwargs.get("impersonate") or self.DEFAULT_IMPERSONATE
        )
        super().__init__(**session_kwargs)
        self.proxy = proxy

    @property
    def user_agent(self) -> str:
        return self.headers["user-agent"]

    @property
    def proxy(self) -> Proxy | None:
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: str | Proxy | None):
        if not proxy:
            self.proxies = {}
            return

        self._proxy = Proxy.from_str(proxy) if proxy else None
        self.proxies = {"http": self._proxy.as_url, "https": self._proxy.as_url}
