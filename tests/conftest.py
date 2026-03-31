"""Shared test fixtures for Windchill SDK tests."""

import pytest

from windchill.config import WindchillConfig


@pytest.fixture
def config() -> WindchillConfig:
    return WindchillConfig(
        base_url="https://windchill.example.com/Windchill/servlet/odata",
        username="testuser",
        password="testpass",
    )


@pytest.fixture
def nonce_token() -> str:
    return "test-nonce-token-abc123"
