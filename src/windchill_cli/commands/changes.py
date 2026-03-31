"""Change management commands for the Windchill CLI."""

from __future__ import annotations

from enum import Enum
from typing import Optional

import typer

from windchill_cli.output import FormatOption, OutputFormat, print_output, print_single

app = typer.Typer(name="changes", help="Manage change objects (ECR, ECN, PR).")

CHANGE_COLUMNS = ["ID", "Name", "Number", "State"]


class ChangeType(str, Enum):
    """Supported change object types."""

    ecr = "ecr"
    ecn = "ecn"
    pr = "pr"


def get_client():
    from windchill import WindchillClient

    return WindchillClient.from_env().sync()


def _list_by_type(wc, change_type: ChangeType, query):
    """Dispatch list call based on change type."""
    dispatch = {
        ChangeType.ecr: wc.change_mgmt.list_change_requests,
        ChangeType.ecn: wc.change_mgmt.list_change_notices,
        ChangeType.pr: wc.change_mgmt.list_problem_reports,
    }
    return dispatch[change_type](query)


def _create_by_type(wc, change_type: ChangeType, name: str, context_id: str | None):
    """Dispatch create call based on change type."""
    kwargs: dict = {"name": name}
    if context_id:
        kwargs["context_id"] = context_id

    dispatch = {
        ChangeType.ecr: wc.change_mgmt.create_change_request,
        ChangeType.ecn: wc.change_mgmt.create_change_notice,
        ChangeType.pr: wc.change_mgmt.create_problem_report,
    }
    return dispatch[change_type](**kwargs)


@app.command("list")
def list_changes(
    change_type: Optional[ChangeType] = typer.Option(None, "--type", help="Change type: ecr, ecn, or pr."),
    filter_expr: Optional[str] = typer.Option(None, "--filter", help="OData $filter expression."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """List change objects, optionally filtered by type."""
    from windchill.odata.filter import FilterExpr
    from windchill.odata.query import Query

    try:
        with get_client() as wc:
            query = Query()
            if filter_expr:
                query = query.filter(FilterExpr(filter_expr))

            if change_type:
                response = _list_by_type(wc, change_type, query)
                title = f"Change Objects ({change_type.value.upper()})"
                print_output(response.items, fmt, columns=CHANGE_COLUMNS, title=title)
            else:
                all_items: list[dict] = []
                for ct in ChangeType:
                    response = _list_by_type(wc, ct, query)
                    for item in response.items:
                        item["Type"] = ct.value.upper()
                    all_items.extend(response.items)
                columns = ["Type"] + CHANGE_COLUMNS
                print_output(all_items, fmt, columns=columns, title="Change Objects")
    except Exception as exc:
        typer.echo(f"Error listing change objects: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("create")
def create_change(
    name: str = typer.Argument(..., help="Change object name."),
    change_type: ChangeType = typer.Option(..., "--type", help="Change type: ecr, ecn, or pr."),
    context_id: Optional[str] = typer.Option(None, "--context-id", help="Container Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Create a new change object."""
    try:
        with get_client() as wc:
            result = _create_by_type(wc, change_type, name, context_id)
            typer.echo(f"{change_type.value.upper()} created successfully.")
            print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error creating change object: {exc}", err=True)
        raise typer.Exit(code=1)
