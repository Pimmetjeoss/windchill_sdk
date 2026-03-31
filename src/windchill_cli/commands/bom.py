"""BOM commands for the Windchill CLI."""

from __future__ import annotations

import typer

from windchill_cli.output import FormatOption, OutputFormat, print_output

app = typer.Typer(name="bom", help="Read bills of materials and where-used data.")

BOM_COLUMNS = ["ID", "Name", "Number", "Quantity", "Unit"]


def get_client():
    from windchill import WindchillClient

    return WindchillClient.from_env().sync()


@app.command("read")
def read_bom(
    part_id: str = typer.Argument(..., help="Part Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Read the bill of materials for a part."""
    try:
        with get_client() as wc:
            response = wc.prod_mgmt.get_bom(part_id)
            print_output(response.items, fmt, columns=BOM_COLUMNS, title="BOM")
    except Exception as exc:
        typer.echo(f"Error reading BOM: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("where-used")
def where_used(
    part_id: str = typer.Argument(..., help="Part Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Show where a part is used."""
    try:
        with get_client() as wc:
            result = wc.prod_mgmt.get_where_used(part_id)
            items = result.get("value", []) if isinstance(result, dict) else []
            print_output(items, fmt, title="Where Used")
    except Exception as exc:
        typer.echo(f"Error getting where-used: {exc}", err=True)
        raise typer.Exit(code=1)
