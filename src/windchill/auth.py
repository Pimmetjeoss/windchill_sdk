"""Authentication providers for Windchill REST API."""

from __future__ import annotations

import asyncio
import base64
import logging
from dataclasses import dataclass

from windchill.config import WindchillConfig

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BasicAuthProvider:
    """Generates Basic Authentication headers from credentials."""

    username: str
    password: str

    @classmethod
    def from_config(cls, config: WindchillConfig) -> BasicAuthProvider:
        return cls(username=config.username, password=config.password)

    @property
    def header_value(self) -> str:
        """Base64-encoded Basic Auth header value."""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("ascii")
        return f"Basic {encoded}"

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": self.header_value}


class NonceManager:
    """Manages CSRF nonce token lifecycle.

    Fetches the nonce token from PTC/GetNonceToken() and caches it
    for the duration of the session. Thread-safe via asyncio Lock.
    """

    def __init__(self, config: WindchillConfig):
        self._config = config
        self._nonce: str | None = None
        self._lock = asyncio.Lock()

    @property
    def cached_nonce(self) -> str | None:
        """Return the currently cached nonce, if any."""
        return self._nonce

    async def get_nonce(self, http_get) -> str:
        """Get a valid CSRF nonce token, fetching a new one if needed.

        Args:
            http_get: Async callable that performs GET request and returns response dict.
                      Signature: async (url: str) -> dict
        """
        async with self._lock:
            if self._nonce is not None:
                return self._nonce
            return await self._fetch_nonce(http_get)

    async def refresh_nonce(self, http_get) -> str:
        """Force-fetch a new CSRF nonce token.

        Args:
            http_get: Async callable that performs GET request and returns response dict.
        """
        async with self._lock:
            return await self._fetch_nonce(http_get)

    def invalidate(self) -> None:
        """Clear the cached nonce, forcing a re-fetch on next use."""
        self._nonce = None

    async def _fetch_nonce(self, http_get) -> str:
        """Fetch nonce token from the Windchill server.

        Tries GetCSRFToken() first (newer servers), falls back to GetNonceToken().
        Token value may be in NonceValue, NonceToken, or value field.
        """
        endpoints = ["GetCSRFToken", "GetNonceToken"]
        for endpoint in endpoints:
            url = f"{self._config.odata_base}/PTC/{endpoint}()"
            logger.debug("Fetching CSRF nonce token from %s", url)
            try:
                response = await http_get(url)
                token = (
                    response.get("NonceValue")
                    or response.get("NonceToken")
                    or response.get("value", "")
                )
                if token:
                    self._nonce = token
                    logger.debug("CSRF nonce token obtained via %s", endpoint)
                    return token
            except Exception:
                logger.debug("Endpoint %s not available, trying next", endpoint)
                continue

        raise ValueError("Failed to obtain CSRF nonce token from server")

        self._nonce = token
        logger.debug("CSRF nonce token obtained successfully")
        return token
