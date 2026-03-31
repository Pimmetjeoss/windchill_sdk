"""Admin commands for the Windchill CLI."""

from __future__ import annotations

from typing import Optional

import typer

from windchill_cli.output import FormatOption, OutputFormat, print_output

app = typer.Typer(name="admin", help="Administrative operations (containers, folders, users).")

CONTAINER_COLUMNS = ["ID", "Name", "ContainerType"]
FOLDER_COLUMNS = ["ID", "Name", "FolderPath"]
USER_COLUMNS = ["ID", "Name", "Email", "DisplayName"]


def get_client():
    from windchill import WindchillClient

    return WindchillClient.from_env().sync()


@app.command("containers")
def list_containers(
    fmt: OutputFormat = FormatOption,
) -> None:
    """List all accessible containers (Products, Libraries, Projects)."""
    try:
        with get_client() as wc:
            response = wc.data_admin.list_containers()
            print_output(response.items, fmt, columns=CONTAINER_COLUMNS, title="Containers")
    except Exception as exc:
        typer.echo(f"Error listing containers: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("folders")
def list_folders(
    container_id: str = typer.Argument(..., help="Container Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """List folders within a container."""
    from windchill.odata.filter import F
    from windchill.odata.query import Query

    try:
        with get_client() as wc:
            query = Query().filter(
                F.eq("Context@odata.bind", f"Containers('{container_id}')")
            )
            response = wc.data_admin.list_folders(query)
            print_output(response.items, fmt, columns=FOLDER_COLUMNS, title="Folders")
    except Exception as exc:
        typer.echo(f"Error listing folders: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("users")
def list_users(
    filter_expr: Optional[str] = typer.Option(None, "--filter", help="OData $filter expression."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """List users."""
    from windchill.odata.filter import FilterExpr
    from windchill.odata.query import Query

    try:
        with get_client() as wc:
            query = Query()
            if filter_expr:
                query = query.filter(FilterExpr(filter_expr))
            response = wc.principal_mgmt.list_users(query)
            print_output(response.items, fmt, columns=USER_COLUMNS, title="Users")
    except Exception as exc:
        typer.echo(f"Error listing users: {exc}", err=True)
        raise typer.Exit(code=1)
