"""CLI commands for Spare Parts Manual generation."""

from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Spare Parts Manual generation")
console = Console()


@app.command("generate")
def generate(
    sap_export: Path = typer.Argument(
        ..., help="Path to SAP BOM export Excel file (.xls/.xlsx)"
    ),
    output_dir: Path = typer.Option(
        None, "--output", "-o", help="Output directory for PDFs (default: temp dir)"
    ),
    drawings_folder: Path = typer.Option(
        None, "--drawings", "-d", help="Folder with TIFF/PDF drawing files"
    ),
    machine_name: str = typer.Option(
        "", "--name", "-n", help="Machine name for titles (e.g. 'CW850')"
    ),
    publish: bool = typer.Option(
        False, "--publish", "-p", help="Upload PDFs to Windchill"
    ),
    context_id: str = typer.Option(
        "", "--context", help="Windchill container ID (for publishing)"
    ),
    service_boms_file: Path = typer.Option(
        None, "--sboms", help="Legacy Service BOMs text file"
    ),
    drawing_master_file: Path = typer.Option(
        None, "--dwg-master", help="Legacy Assembly Drawing master data file"
    ),
    no_windchill: bool = typer.Option(
        False, "--no-windchill", help="Skip Windchill connection (offline mode)"
    ),
) -> None:
    """Generate MSPM + ESPM spare parts manuals from SAP BOM export.

    Reads the SAP BOM export, enriches with Windchill data (BOMs, drawings),
    and generates both Mechanical and Electrical spare parts manual PDFs.

    Examples:

        wc spm generate DifBook.xls --output ./output --name "CW850"

        wc spm generate export.xlsx --drawings ./tiffs --publish

        wc spm generate export.xlsx --sboms SBOMs.txt --dwg-master dwg.txt
    """
    asyncio.run(
        _generate_async(
            sap_export,
            output_dir,
            drawings_folder,
            machine_name,
            publish,
            context_id,
            service_boms_file,
            drawing_master_file,
            no_windchill,
        )
    )


async def _generate_async(
    sap_export: Path,
    output_dir: Path | None,
    drawings_folder: Path | None,
    machine_name: str,
    publish: bool,
    context_id: str,
    service_boms_file: Path | None,
    drawing_master_file: Path | None,
    no_windchill: bool,
) -> None:
    """Async implementation of the generate command."""
    from windchill_spm.pipeline import generate_spm

    client = None
    if not no_windchill:
        try:
            from windchill import WindchillClient, WindchillConfig

            config = WindchillConfig.from_env()
            client = WindchillClient(config)
            console.print("[green]Connected to Windchill[/green]")
        except Exception as exc:
            console.print(f"[yellow]Windchill not available: {exc}[/yellow]")
            console.print("[yellow]Running in offline mode[/yellow]")

    with console.status("Generating Spare Parts Manuals..."):
        result = await generate_spm(
            sap_export,
            client=client,
            drawings_folder=str(drawings_folder) if drawings_folder else None,
            output_dir=str(output_dir) if output_dir else None,
            publish=publish,
            context_id=context_id or None,
            machine_name=machine_name,
            service_boms_file=str(service_boms_file) if service_boms_file else None,
            drawing_master_file=str(drawing_master_file) if drawing_master_file else None,
        )

    # Display results
    console.print()
    if result.mspm_pdf_path:
        size_mb = result.mspm_pdf_path.stat().st_size / (1024 * 1024)
        console.print(f"[green]MSPM:[/green] {result.mspm_pdf_path} ({size_mb:.1f} MB)")
        if result.mspm_wh_number:
            console.print(f"  Published as: {result.mspm_wh_number}")

    if result.espm_pdf_path:
        size_mb = result.espm_pdf_path.stat().st_size / (1024 * 1024)
        console.print(f"[green]ESPM:[/green] {result.espm_pdf_path} ({size_mb:.1f} MB)")
        if result.espm_wh_number:
            console.print(f"  Published as: {result.espm_wh_number}")

    if result.warnings:
        console.print()
        for warning in result.warnings:
            console.print(f"[yellow]Warning:[/yellow] {warning}")

    if not result.mspm_pdf_path and not result.espm_pdf_path:
        console.print("[red]No manuals generated — check input data[/red]")
        raise typer.Exit(1)
