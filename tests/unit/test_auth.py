"""Tests for authentication providers."""

import base64

import pytest

from windchill.auth import BasicAuthProvider, NonceManager
from windchill.config import WindchillConfig


class TestBasicAuthProvider:
    def test_header_value(self):
        auth = BasicAuthProvider(username="admin", password="secret")
        expected = base64.b64encode(b"admin:secret").decode("ascii")
        assert auth.header_value == f"Basic {expected}"

    def test_headers_dict(self):
        auth = BasicAuthProvider(username="user", password="pass")
        headers = auth.headers
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("Basic ")

    def test_from_config(self):
        config = WindchillConfig(
            base_url="https://example.com/Windchill/servlet/odata",
            username="testuser",
            password="testpass",
        )
        auth = BasicAuthProvider.from_config(config)
        assert auth.username == "testuser"
        assert auth.password == "testpass"

    def test_special_characters_in_password(self):
        auth = BasicAuthProvider(username="user", password="p@ss:w0rd!")
        decoded = base64.b64decode(
            auth.header_value.replace("Basic ", "")
        ).decode("utf-8")
        assert decoded == "user:p@ss:w0rd!"


class TestNonceManager:
    def test_initial_state(self):
        config = WindchillConfig(
            base_url="https://example.com/Windchill/servlet/odata",
            username="user",
            password="pass",
        )
        manager = NonceManager(config)
        assert manager.cached_nonce is None

    @pytest.mark.asyncio
    async def test_get_nonce(self):
        config = WindchillConfig(
            base_url="https://example.com/Windchill/servlet/odata",
            username="user",
            password="pass",
        )
        manager = NonceManager(config)

        async def mock_get(url: str) -> dict:
            assert "GetNonceToken" in url
            return {"NonceToken": "abc123"}

        token = await manager.get_nonce(mock_get)
        assert token == "abc123"
        assert manager.cached_nonce == "abc123"

    @pytest.mark.asyncio
    async def test_nonce_is_cached(self):
        config = WindchillConfig(
            base_url="https://example.com/Windchill/servlet/odata",
            username="user",
            password="pass",
        )
        manager = NonceManager(config)
        call_count = 0

        async def mock_get(url: str) -> dict:
            nonlocal call_count
            call_count += 1
            return {"NonceToken": "cached_token"}

        await manager.get_nonce(mock_get)
        await manager.get_nonce(mock_get)
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_invalidate_clears_cache(self):
        config = WindchillConfig(
            base_url="https://example.com/Windchill/servlet/odata",
            username="user",
            password="pass",
        )
        manager = NonceManager(config)

        async def mock_get(url: str) -> dict:
            return {"NonceToken": "token"}

        await manager.get_nonce(mock_get)
        manager.invalidate()
        assert manager.cached_nonce is None

    @pytest.mark.asyncio
    async def test_refresh_fetches_new_token(self):
        config = WindchillConfig(
            base_url="https://example.com/Windchill/servlet/odata",
            username="user",
            password="pass",
        )
        manager = NonceManager(config)
        call_count = 0

        async def mock_get(url: str) -> dict:
            nonlocal call_count
            call_count += 1
            return {"NonceToken": f"token_{call_count}"}

        await manager.get_nonce(mock_get)
        new_token = await manager.refresh_nonce(mock_get)
        assert new_token == "token_2"
        assert call_count == 2
