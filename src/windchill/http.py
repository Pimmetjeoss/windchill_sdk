"""HTTP transport layer for Windchill REST API."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from windchill.auth import BasicAuthProvider, NonceManager
from windchill.config import WindchillConfig
from windchill.errors import raise_for_status

logger = logging.getLogger(__name__)

WRITE_METHODS = frozenset({"POST", "PATCH", "PUT", "DELETE"})
RETRYABLE_STATUS_CODES = frozenset({429, 503})
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0


class HttpTransport:
    """Async HTTP transport with automatic auth, CSRF nonce, and retry logic."""

    def __init__(self, config: WindchillConfig):
        self._config = config
        self._auth = BasicAuthProvider.from_config(config)
        self._nonce_manager = NonceManager(config)
        self._client: httpx.AsyncClient | None = None

    @property
    def nonce_manager(self) -> NonceManager:
        return self._nonce_manager

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                verify=self._config.verify_ssl,
                timeout=httpx.Timeout(self._config.timeout),
                follow_redirects=True,
            )
        return self._client

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    def _base_headers(self) -> dict[str, str]:
        return {
            **self._auth.headers,
            "Accept": "application/json",
        }

    async def _add_nonce_header(self, headers: dict[str, str]) -> dict[str, str]:
        """Add CSRF nonce header for write operations."""
        nonce = await self._nonce_manager.get_nonce(self._raw_get_json)
        return {**headers, "CSRF_NONCE": nonce}

    async def _raw_get_json(self, url: str) -> dict[str, Any]:
        """Perform a raw GET request (used by NonceManager to avoid circular dep)."""
        client = await self._ensure_client()
        response = await client.get(url, headers=self._base_headers())
        if response.status_code >= 400:
            body = response.json() if response.content else None
            raise_for_status(response.status_code, body)
        return response.json()

    async def request(
        self,
        method: str,
        url: str,
        *,
        json: dict[str, Any] | list | None = None,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
        content_type: str | None = None,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Execute an HTTP request with auth, nonce, and retry handling.

        Returns the raw httpx.Response for cases where callers need
        access to headers or status codes (e.g., batch, file download).
        """
        client = await self._ensure_client()
        request_headers = self._base_headers()

        if headers:
            request_headers.update(headers)

        if content_type:
            request_headers["Content-Type"] = content_type

        if method.upper() in WRITE_METHODS:
            request_headers = await self._add_nonce_header(request_headers)
            if "Content-Type" not in request_headers and json is not None:
                request_headers["Content-Type"] = "application/json"

        for attempt in range(MAX_RETRIES + 1):
            logger.debug("%s %s (attempt %d)", method, url, attempt + 1)

            kwargs: dict[str, Any] = {"headers": request_headers, "params": params}
            if json is not None:
                kwargs["json"] = json
            elif data is not None:
                kwargs["content"] = data

            response = await client.request(method, url, **kwargs)

            if response.status_code in RETRYABLE_STATUS_CODES and attempt < MAX_RETRIES:
                backoff = INITIAL_BACKOFF * (2**attempt)
                logger.warning(
                    "Retryable status %d, backing off %.1fs",
                    response.status_code,
                    backoff,
                )
                await asyncio.sleep(backoff)
                continue

            # If nonce expired (403 on write), refresh and retry once
            if (
                response.status_code == 403
                and method.upper() in WRITE_METHODS
                and attempt == 0
            ):
                logger.debug("Got 403 on write, refreshing CSRF nonce and retrying")
                self._nonce_manager.invalidate()
                request_headers = await self._add_nonce_header(request_headers)
                continue

            break

        return response

    async def get_json(
        self,
        url: str,
        *,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """GET request returning parsed JSON."""
        response = await self.request("GET", url, params=params)
        body = response.json() if response.content else {}
        raise_for_status(response.status_code, body)
        return body

    async def post_json(
        self,
        url: str,
        body: dict[str, Any] | list | None = None,
    ) -> dict[str, Any]:
        """POST request with JSON body, returning parsed JSON."""
        response = await self.request("POST", url, json=body or {})
        if response.status_code == 204:
            return {}
        resp_body = response.json() if response.content else {}
        raise_for_status(response.status_code, resp_body)
        return resp_body

    async def patch_json(
        self,
        url: str,
        body: dict[str, Any],
    ) -> dict[str, Any]:
        """PATCH request with JSON body, returning parsed JSON."""
        response = await self.request("PATCH", url, json=body)
        if response.status_code == 204:
            return {}
        resp_body = response.json() if response.content else {}
        raise_for_status(response.status_code, resp_body)
        return resp_body

    async def delete(self, url: str) -> None:
        """DELETE request."""
        response = await self.request("DELETE", url)
        if response.status_code not in (200, 204):
            body = response.json() if response.content else {}
            raise_for_status(response.status_code, body)

    async def get_bytes(self, url: str) -> tuple[bytes, dict[str, str]]:
        """GET request returning raw bytes and response headers (for file downloads)."""
        response = await self.request("GET", url)
        raise_for_status(response.status_code, None)
        return response.content, dict(response.headers)

    async def download_content_url(self, url: str) -> tuple[bytes, dict[str, str]]:
        """Download file content from a Windchill signed download URL.

        Establishes a session first (via CSRF token fetch) to ensure
        the signed URL works with proper cookies.
        """
        client = await self._ensure_client()
        headers = self._base_headers()

        # Ensure session is established (fetches JSESSIONID cookie)
        await self._nonce_manager.get_nonce(self._raw_get_json)

        # Download with auth headers (cookies are managed by httpx client)
        response = await client.get(url, headers=headers)

        if response.status_code >= 400:
            body = response.json() if response.content else None
            raise_for_status(response.status_code, body)

        return response.content, dict(response.headers)
