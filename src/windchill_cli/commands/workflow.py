"""Workflow commands for the Windchill CLI."""

from __future__ import annotations

from typing import Optional

import typer

from windchill_cli.output import FormatOption, OutputFormat, print_output, print_single

app = typer.Typer(name="workflow", help="Manage workflow work items.")

WORKITEM_COLUMNS = ["ID", "Name", "State", "AssignedTo", "CreatedOn"]


def get_client():
    from windchill import WindchillClient

    return WindchillClient.from_env().sync()


@app.command("list")
def list_workitems(
    filter_expr: Optional[str] = typer.Option(None, "--filter", help="OData $filter expression."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """List workflow work items."""
    from windchill.odata.filter import FilterExpr
    from windchill.odata.query import Query

    try:
        with get_client() as wc:
            query = Query()
            if filter_expr:
                query = query.filter(FilterExpr(filter_expr))
            response = wc.workflow.list_workitems(query)
            print_output(response.items, fmt, columns=WORKITEM_COLUMNS, title="Work Items")
    except Exception as exc:
        typer.echo(f"Error listing work items: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("complete")
def complete_workitem(
    workitem_id: str = typer.Argument(..., help="Work item Object Reference ID."),
    routing_option: Optional[str] = typer.Option(None, "--routing-option", help="Routing option name."),
    comment: Optional[str] = typer.Option(None, "--comment", help="Completion comment."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Complete a workflow work item."""
    try:
        with get_client() as wc:
            result = wc.workflow.complete_workitem(
                workitem_id,
                routing_option=routing_option,
                comment=comment,
            )
            typer.echo("Work item completed successfully.")
            print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error completing work item: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("reassign")
def reassign_workitem(
    workitem_id: str = typer.Argument(..., help="Work item Object Reference ID."),
    user_id: str = typer.Argument(..., help="User ID to reassign to."),
    comment: Optional[str] = typer.Option(None, "--comment", help="Reassignment comment."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Reassign a workflow work item to another user."""
    try:
        with get_client() as wc:
            result = wc.workflow.reassign_workitem(
                workitem_id,
                user_id,
                comment=comment,
            )
            typer.echo(f"Work item reassigned to '{user_id}'.")
            print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error reassigning work item: {exc}", err=True)
        raise typer.Exit(code=1)
