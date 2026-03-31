"""Windchill CLI - main entry point."""

from __future__ import annotations

import os

import typer
from rich.console import Console
from rich.table import Table

from windchill_cli.commands.admin import app as admin_app
from windchill_cli.commands.bom import app as bom_app
from windchill_cli.commands.changes import app as changes_app
from windchill_cli.commands.documents import app as docs_app
from windchill_cli.commands.parts import app as parts_app
from windchill_cli.commands.search import app as search_app
from windchill_cli.commands.workflow import app as workflow_app

app = typer.Typer(
    name="wc",
    help="Windchill PLM CLI - command-line interface for PTC Windchill.",
    no_args_is_help=True,
)

app.add_typer(parts_app, name="parts")
app.add_typer(docs_app, name="docs")
app.add_typer(bom_app, name="bom")
app.add_typer(changes_app, name="changes")
app.add_typer(workflow_app, name="workflow")
app.add_typer(search_app, name="search")
app.add_typer(admin_app, name="admin")

console = Console()

ENV_PREFIX = "WINDCHILL"
CONFIG_KEYS = [
    ("BASE_URL", "Windchill OData base URL", True),
    ("USERNAME", "Username for authentication", True),
    ("PASSWORD", "Password for authentication", True),
    ("VERIFY_SSL", "Verify SSL certificates", False),
    ("TIMEOUT", "Request timeout in seconds", False),
    ("MAX_PAGE_SIZE", "Max items per page", False),
    ("API_VERSION", "API version", False),
]


@app.command("config")
def show_config() -> None:
    """Show current Windchill CLI configuration from environment variables."""
    table = Table(title="Windchill CLI Configuration")
    table.add_column("Variable", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Required", style="yellow")

    for key, description, required in CONFIG_KEYS:
        env_var = f"{ENV_PREFIX}_{key}"
        value = os.environ.get(env_var, "")
        display_value = _mask_secret(value) if "PASSWORD" in key else (value or "(not set)")
        req_label = "Yes" if required else "No"
        table.add_row(env_var, display_value, req_label)

    console.print(table)


def _mask_secret(value: str) -> str:
    """Mask a secret value for display."""
    if not value:
        return "(not set)"
    if len(value) <= 4:
        return "****"
    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def main() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
