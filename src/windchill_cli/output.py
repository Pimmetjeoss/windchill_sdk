"""Output formatters for the Windchill CLI."""

from __future__ import annotations

import csv
import io
import json
from enum import Enum
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

console = Console()


class OutputFormat(str, Enum):
    """Supported output formats."""

    table = "table"
    json = "json"
    csv = "csv"


FormatOption = typer.Option(
    OutputFormat.table,
    "--format",
    "-f",
    help="Output format (table, json, csv).",
)


def format_table(
    items: list[dict[str, Any]],
    columns: list[str] | None = None,
    title: str | None = None,
) -> str:
    """Render items as a Rich table and return the string representation."""
    if not items:
        return "No results found."

    resolved_columns = columns or list(items[0].keys())
    table = Table(title=title, show_lines=False)

    for col in resolved_columns:
        table.add_column(col, overflow="fold")

    for item in items:
        row = [str(item.get(col, "")) for col in resolved_columns]
        table.add_row(*row)

    buf = io.StringIO()
    temp_console = Console(file=buf, width=200, force_terminal=False)
    temp_console.print(table)
    return buf.getvalue()


def format_json(data: Any) -> str:
    """Render data as pretty-printed JSON."""
    return json.dumps(data, indent=2, default=str)


def format_csv(
    items: list[dict[str, Any]],
    columns: list[str] | None = None,
) -> str:
    """Render items as CSV text."""
    if not items:
        return ""

    resolved_columns = columns or list(items[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=resolved_columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(items)
    return buf.getvalue()


def _print_table(
    items: list[dict[str, Any]],
    columns: list[str] | None = None,
    title: str | None = None,
) -> None:
    """Print items as a Rich table directly to the console."""
    if not items:
        console.print("No results found.")
        return

    resolved_columns = columns or list(items[0].keys())
    table = Table(title=title, show_lines=False)

    for col in resolved_columns:
        table.add_column(col, overflow="fold")

    for item in items:
        row = [str(item.get(col, "")) for col in resolved_columns]
        table.add_row(*row)

    console.print(table)


def print_output(
    items: list[dict[str, Any]],
    fmt: OutputFormat,
    columns: list[str] | None = None,
    title: str | None = None,
) -> None:
    """Print items in the requested format to the console."""
    if fmt == OutputFormat.json:
        typer.echo(format_json(items))
    elif fmt == OutputFormat.csv:
        typer.echo(format_csv(items, columns))
    else:
        _print_table(items, columns, title)


def print_single(
    item: dict[str, Any],
    fmt: OutputFormat,
) -> None:
    """Print a single entity in the requested format."""
    if fmt == OutputFormat.json:
        typer.echo(format_json(item))
    elif fmt == OutputFormat.csv:
        typer.echo(format_csv([item]))
    else:
        _print_table([item])
