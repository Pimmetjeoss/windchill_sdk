"""Configuration management for Windchill SDK."""

from __future__ import annotations

import os
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class WindchillConfig:
    """Immutable configuration for connecting to a Windchill server.

    Can be created directly, from environment variables, or from a config file.
    """

    base_url: str
    username: str
    password: str
    verify_ssl: bool = True
    timeout: float = 30.0
    max_page_size: int = 100
    api_version: str | None = None

    @classmethod
    def from_env(cls, prefix: str = "WINDCHILL") -> WindchillConfig:
        """Create config from environment variables.

        Reads:
            {prefix}_BASE_URL - Windchill OData base URL
            {prefix}_USERNAME - Username for Basic Auth
            {prefix}_PASSWORD - Password for Basic Auth
            {prefix}_VERIFY_SSL - Whether to verify SSL (default: true)
            {prefix}_TIMEOUT - Request timeout in seconds (default: 30)
            {prefix}_MAX_PAGE_SIZE - Max items per page (default: 100)
            {prefix}_API_VERSION - API version (default: None)
        """
        base_url = os.environ.get(f"{prefix}_BASE_URL")
        username = os.environ.get(f"{prefix}_USERNAME")
        password = os.environ.get(f"{prefix}_PASSWORD")

        if not base_url:
            raise ValueError(f"{prefix}_BASE_URL environment variable is required")
        if not username:
            raise ValueError(f"{prefix}_USERNAME environment variable is required")
        if not password:
            raise ValueError(f"{prefix}_PASSWORD environment variable is required")

        return cls(
            base_url=base_url.rstrip("/"),
            username=username,
            password=password,
            verify_ssl=os.environ.get(f"{prefix}_VERIFY_SSL", "true").lower() == "true",
            timeout=float(os.environ.get(f"{prefix}_TIMEOUT", "30")),
            max_page_size=int(os.environ.get(f"{prefix}_MAX_PAGE_SIZE", "100")),
            api_version=os.environ.get(f"{prefix}_API_VERSION"),
        )

    def with_overrides(self, **kwargs) -> WindchillConfig:
        """Return a new config with specified fields overridden."""
        return replace(self, **kwargs)

    @property
    def odata_base(self) -> str:
        """Base URL for OData requests, including version if specified."""
        if self.api_version:
            return f"{self.base_url}/v{self.api_version}"
        return self.base_url

    def domain_url(self, domain: str) -> str:
        """Build the full URL for a domain endpoint."""
        return f"{self.odata_base}/{domain}"
