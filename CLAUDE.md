# Windchill SDK

Python SDK + MCP Server + CLI for PTC Windchill REST API v1.6 (OData v4).

## Project Structure

- `src/windchill/` - Core SDK (async-first, sync wrappers)
- `src/windchill_mcp/` - MCP server for AI agent integration
- `src/windchill_cli/` - CLI tool (`wc` command)
- `tests/` - Unit, integration, and MCP tests

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/
```

## Architecture Rules

- **Immutable data**: Use frozen dataclasses, never mutate
- **Async-first**: All SDK methods are async, sync wrappers provided
- **Small files**: 200-400 lines typical, 800 max
- **Domain pattern**: Each Windchill domain = one module inheriting BaseDomain
- **No hardcoded secrets**: Config via env vars or config file

## Key Patterns

- OData query builder: `Query().filter(F.eq("State", "INWORK")).top(10)`
- CSRF nonce: Automatically fetched and cached by NonceManager
- Auto-paging: `async for page in client.paginate(...)`
- Batch: `Batch(domain).begin_changeset().post(...).end_changeset()`

## Environment Variables

- `WINDCHILL_BASE_URL` - Windchill server OData base URL
- `WINDCHILL_USERNAME` - Username for Basic Auth
- `WINDCHILL_PASSWORD` - Password for Basic Auth
