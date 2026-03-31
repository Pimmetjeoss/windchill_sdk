"""Search commands for the Windchill CLI."""

from __future__ import annotations

from typing import Optional

import typer

from windchill_cli.output import FormatOption, OutputFormat, print_output

app = typer.Typer(name="search", help="Search Windchill objects by keyword.")

SEARCH_COLUMNS = ["ID", "Name", "Number", "State", "@odata.type"]


def get_client():
    from windchill import WindchillClient

    return WindchillClient.from_env().sync()


@app.callback(invoke_without_command=True)
def search(
    keyword: str = typer.Argument(..., help="Keyword to search for."),
    top: Optional[int] = typer.Option(None, "--top", help="Max number of results."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Search Windchill objects by keyword."""
    from windchill.odata.query import Query

    try:
        with get_client() as wc:
            query = Query()
            if top:
                query = query.top(top)
            response = wc.common.search_by_keyword(keyword, query=query)
            print_output(response.items, fmt, columns=SEARCH_COLUMNS, title=f"Search: {keyword}")
    except Exception as exc:
        typer.echo(f"Error searching: {exc}", err=True)
        raise typer.Exit(code=1)
