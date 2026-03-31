"""WindchillClient - main entry point for the Windchill SDK."""

from __future__ import annotations

import asyncio
from typing import Any, Self

from windchill.config import WindchillConfig
from windchill.domains.cad_doc_mgmt import CADDocMgmt
from windchill.domains.capa import CAPA
from windchill.domains.cem import CEM
from windchill.domains.change_mgmt import ChangeMgmt
from windchill.domains.clf_structure import ClfStructure
from windchill.domains.common import Common
from windchill.domains.data_admin import DataAdmin
from windchill.domains.doc_mgmt import DocMgmt
from windchill.domains.effectivity_mgmt import EffectivityMgmt
from windchill.domains.event_mgmt import EventMgmt
from windchill.domains.mfg_process_mgmt import MfgProcessMgmt
from windchill.domains.nc import NC
from windchill.domains.pdm import PDM
from windchill.domains.principal_mgmt import PrincipalMgmt
from windchill.domains.prod_mgmt import ProdMgmt
from windchill.domains.prod_platform_mgmt import ProdPlatformMgmt
from windchill.domains.qms import QMS
from windchill.domains.saved_search import SavedSearch
from windchill.domains.supplier_mgmt import SupplierMgmt
from windchill.domains.visualization import Visualization
from windchill.domains.workflow import Workflow
from windchill.http import HttpTransport
from windchill.odata.batch import Batch


class WindchillClient:
    """Main client for interacting with the Windchill REST API.

    Provides access to all domain services and convenience methods
    for common operations.

    Usage (async):
        async with WindchillClient.from_env() as wc:
            parts = await wc.prod_mgmt.list_parts(Query().top(10))

    Usage (sync):
        with WindchillClient.from_env().sync() as wc:
            parts = wc.prod_mgmt.list_parts(Query().top(10))
    """

    def __init__(self, config: WindchillConfig):
        self._config = config
        self._http = HttpTransport(config)

        # Domain services
        self.common = Common(self._http)
        self.prod_mgmt = ProdMgmt(self._http)
        self.doc_mgmt = DocMgmt(self._http)
        self.change_mgmt = ChangeMgmt(self._http)
        self.cad_doc_mgmt = CADDocMgmt(self._http)
        self.data_admin = DataAdmin(self._http)
        self.principal_mgmt = PrincipalMgmt(self._http)
        self.workflow = Workflow(self._http)
        self.effectivity_mgmt = EffectivityMgmt(self._http)
        self.event_mgmt = EventMgmt(self._http)
        self.supplier_mgmt = SupplierMgmt(self._http)
        self.qms = QMS(self._http)
        self.capa = CAPA(self._http)
        self.nc = NC(self._http)
        self.cem = CEM(self._http)
        self.mfg_process_mgmt = MfgProcessMgmt(self._http)
        self.prod_platform_mgmt = ProdPlatformMgmt(self._http)
        self.clf_structure = ClfStructure(self._http)
        self.visualization = Visualization(self._http)
        self.saved_search = SavedSearch(self._http)
        self.pdm = PDM(self._http)

    @classmethod
    def from_env(cls, prefix: str = "WINDCHILL") -> WindchillClient:
        """Create a client from environment variables."""
        config = WindchillConfig.from_env(prefix)
        return cls(config)

    @property
    def config(self) -> WindchillConfig:
        return self._config

    @property
    def http(self) -> HttpTransport:
        return self._http

    # ── Context Manager (async) ──

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc_info) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    # ── Convenience Methods ──

    async def get_metadata(self, domain: str) -> str:
        """Fetch the EDM $metadata XML for a domain."""
        url = f"{self._config.domain_url(domain)}/$metadata"
        response = await self._http.request("GET", url)
        return response.text

    async def get_service_document(self, domain: str) -> dict[str, Any]:
        """Fetch the OData service document listing entity sets for a domain."""
        url = self._config.domain_url(domain)
        return await self._http.get_json(url)

    def batch(self, domain: str) -> Batch:
        """Create a new batch request builder for a domain."""
        return Batch(domain)

    async def execute_batch(self, batch: Batch) -> Any:
        """Execute a batch request and return the raw response."""
        content_type, body = batch.build()
        url = self._config.domain_url(batch.domain) + "/$batch"
        response = await self._http.request(
            "POST",
            url,
            data=body.encode("utf-8"),
            content_type=content_type,
        )
        return response

    # ── Sync Wrapper ──

    def sync(self) -> SyncWindchillClient:
        """Return a synchronous wrapper around this async client."""
        return SyncWindchillClient(self)


class SyncWindchillClient:
    """Synchronous wrapper around WindchillClient.

    Runs async methods in an event loop for synchronous code.

    Usage:
        with WindchillClient.from_env().sync() as wc:
            parts = wc.prod_mgmt.list_parts(Query().top(10))
    """

    def __init__(self, async_client: WindchillClient):
        self._async_client = async_client
        self._loop: asyncio.AbstractEventLoop | None = None

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None or self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
        return self._loop

    def _run(self, coro):
        return self._get_loop().run_until_complete(coro)

    def __enter__(self) -> SyncWindchillClient:
        return self

    def __exit__(self, *exc_info) -> None:
        self._run(self._async_client.close())
        if self._loop and not self._loop.is_closed():
            self._loop.close()

    def __getattr__(self, name: str):
        """Proxy attribute access to the async client's domain services.

        Domain service method calls are automatically wrapped to run synchronously.
        """
        attr = getattr(self._async_client, name)

        if hasattr(attr, '__class__') and hasattr(attr.__class__, 'domain'):
            # It's a domain service - wrap it
            return _SyncDomainProxy(attr, self._run)

        return attr


class _SyncDomainProxy:
    """Wraps an async domain service to make its methods synchronous."""

    def __init__(self, domain, runner):
        self._domain = domain
        self._runner = runner

    def __getattr__(self, name: str):
        attr = getattr(self._domain, name)
        if callable(attr) and asyncio.iscoroutinefunction(attr):
            def sync_wrapper(*args, **kwargs):
                return self._runner(attr(*args, **kwargs))
            sync_wrapper.__name__ = name
            sync_wrapper.__doc__ = attr.__doc__
            return sync_wrapper
        return attr
