"""Document commands for the Windchill CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from windchill_cli.output import FormatOption, OutputFormat, print_output, print_single

app = typer.Typer(name="docs", help="Manage Windchill documents.")

DOC_COLUMNS = ["ID", "Name", "Number", "State", "Version"]


def get_client():
    from windchill import WindchillClient

    return WindchillClient.from_env().sync()


@app.command("list")
def list_documents(
    filter_expr: Optional[str] = typer.Option(None, "--filter", help="OData $filter expression."),
    top: Optional[int] = typer.Option(None, "--top", help="Max number of results."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """List documents with optional filtering."""
    from windchill.odata.filter import FilterExpr
    from windchill.odata.query import Query

    try:
        with get_client() as wc:
            query = Query()
            if filter_expr:
                query = query.filter(FilterExpr(filter_expr))
            if top:
                query = query.top(top)
            response = wc.doc_mgmt.list_documents(query)
            print_output(response.items, fmt, columns=DOC_COLUMNS, title="Documents")
    except Exception as exc:
        typer.echo(f"Error listing documents: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("get")
def get_document(
    doc_id: str = typer.Argument(..., help="Document Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Get a single document by ID."""
    try:
        with get_client() as wc:
            doc = wc.doc_mgmt.get_document(doc_id)
            print_single(doc, fmt)
    except Exception as exc:
        typer.echo(f"Error getting document: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("create")
def create_document(
    name: str = typer.Argument(..., help="Document name."),
    context_id: Optional[str] = typer.Option(None, "--context-id", help="Container Object Reference ID."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Create a new document."""
    try:
        with get_client() as wc:
            doc = wc.doc_mgmt.create_document(name, context_id=context_id)
            typer.echo("Document created successfully.")
            print_single(doc, fmt)
    except Exception as exc:
        typer.echo(f"Error creating document: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("upload")
def upload_content(
    working_copy_id: str = typer.Argument(..., help="Working copy Object Reference ID."),
    file_path: Path = typer.Argument(..., help="Path to the file to upload.", exists=True),
    role: str = typer.Option("PRIMARY", "--role", help="Content role (PRIMARY or SECONDARY)."),
    fmt: OutputFormat = FormatOption,
) -> None:
    """Upload file content to a document working copy."""
    try:
        with get_client() as wc:
            result = wc.doc_mgmt.upload_content(
                working_copy_id,
                file_path,
                role=role,
            )
            typer.echo(f"File '{file_path.name}' uploaded successfully.")
            if result:
                print_single(result, fmt)
    except Exception as exc:
        typer.echo(f"Error uploading content: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("download")
def download_document(
    doc_id: str = typer.Argument(..., help="Document Object Reference ID."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path."),
) -> None:
    """Download the primary content of a document."""
    try:
        with get_client() as wc:
            output_path = output or Path(f"./{doc_id}_download")
            saved = wc.doc_mgmt.download_primary(doc_id, output_path)
            typer.echo(f"Downloaded to {saved}")
    except Exception as exc:
        typer.echo(f"Error downloading document: {exc}", err=True)
        raise typer.Exit(code=1)
