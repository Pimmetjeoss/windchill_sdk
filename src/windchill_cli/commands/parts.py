"""Parts commands for the Windchill CLI."""

from __future__ import annotations

from typing import Optional

import typer

from windchill_cli.output import FormatOption, OutputFormat, print_output, print_single

app = typer.Typer(name="parts", help="Manage Windchill parts.")

PART_COLUMNS = ["ID", "Name", "Number", "State", "Version", "Source"]


def get_client():
    from windchill import WindchillClient

    return WindchillClient.from_env().sync()


@app.command("list")
def list_parts(
    filter_expr: Optional[str] = typer.Option(None, "--filter", help="OData $filter expression."),
    top: Optional[int] = typer.Option(None, "--top", help="Max number of results."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """List parts with optional filtering."""
    from windchill.odata.filter import FilterExpr
    from windchill.odata.query import Query

    try:
        with get_client() as wc:
            query = Query()
            if filter_expr:
                query = query.filter(FilterExpr(filter_expr))
            if top:
                query = query.top(top)
            response = wc.prod_mgmt.list_parts(query)
            print_output(response.items, fmt, columns=PART_COLUMNS, title="Parts")
    except Exception as exc:
        typer.echo(f"Error listing parts: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("get")
def get_part(
    part_id: str = typer.Argument(..., help="Part Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Get a single part by ID."""
    try:
        with get_client() as wc:
            part = wc.prod_mgmt.get_part(part_id)
            print_single(part, fmt)
    except Exception as exc:
        typer.echo(f"Error getting part: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("create")
def create_part(
    name: str = typer.Argument(..., help="Part name."),
    number: Optional[str] = typer.Option(None, "--number", help="Part number (auto-generated if omitted)."),
    context_id: Optional[str] = typer.Option(None, "--context-id", help="Container Object Reference ID."),
    source: Optional[str] = typer.Option(None, "--source", help="Part source type (e.g., MAKE, BUY)."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Create a new part."""
    try:
        with get_client() as wc:
            part = wc.prod_mgmt.create_part(
                name,
                number=number,
                context_id=context_id,
                source=source,
            )
            typer.echo("Part created successfully.")
            print_single(part, fmt)
    except Exception as exc:
        typer.echo(f"Error creating part: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("checkout")
def checkout_part(
    part_id: str = typer.Argument(..., help="Part Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Check out a part."""
    try:
        with get_client() as wc:
            result = wc.prod_mgmt.checkout_part(part_id)
            typer.echo("Part checked out successfully.")
            print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error checking out part: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("checkin")
def checkin_part(
    part_id: str = typer.Argument(..., help="Working copy Object Reference ID."),
    comment: Optional[str] = typer.Option(None, "--comment", help="Check-in comment."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Check in a part working copy."""
    try:
        with get_client() as wc:
            result = wc.prod_mgmt.checkin_part(part_id, comment=comment)
            typer.echo("Part checked in successfully.")
            print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error checking in part: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("revise")
def revise_part(
    part_id: str = typer.Argument(..., help="Part Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Create a new revision of a part."""
    try:
        with get_client() as wc:
            result = wc.prod_mgmt.revise_part(part_id)
            typer.echo("Part revised successfully.")
            print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error revising part: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("set-state")
def set_state(
    part_id: str = typer.Argument(..., help="Part Object Reference ID."),
    state: str = typer.Argument(..., help="Lifecycle state (e.g., INWORK, RELEASED)."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Set the lifecycle state of a part."""
    try:
        with get_client() as wc:
            result = wc.prod_mgmt.set_part_state(part_id, state)
            typer.echo(f"Part state set to '{state}'.")
            print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error setting part state: {exc}", err=True)
        raise typer.Exit(code=1)
