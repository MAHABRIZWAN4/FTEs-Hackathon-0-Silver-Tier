#!/usr/bin/env python3
"""
Quick Test Script - Colorful Terminal UI
Run this to see all the colorful features in action!
"""

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    import time

    console = Console()

    # Banner
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🎨 COLORFUL UI TEST[/bold cyan]\n"
        "[dim]Silver Tier AI Employee[/dim]\n"
        "[yellow]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/yellow]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()

    # Status messages
    console.print("[bold green]✓[/bold green] [green]Success message example[/green]")
    console.print("[bold red]✗[/bold red] [red]Error message example[/red]")
    console.print("[bold yellow]⚠[/bold yellow] [yellow]Warning message example[/yellow]")
    console.print("[bold cyan]ℹ[/bold cyan] [cyan]Info message example[/cyan]")
    console.print()

    # Table
    table = Table(title="📊 Sample Summary", border_style="cyan", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", justify="left")
    table.add_column("Count", style="green", justify="center")
    table.add_row("✓ Processed", "[bold green]5[/bold green]")
    table.add_row("⏭ Skipped", "[yellow]2[/yellow]")
    table.add_row("📁 Total", "[bold cyan]7[/bold cyan]")
    console.print(table)
    console.print()

    # Progress bar
    console.print("[cyan]Testing progress bar...[/cyan]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[cyan]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task("[yellow]Processing...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.02)
    console.print()

    # Final panel
    console.print(Panel(
        "[bold green]✓ All colorful features working![/bold green]\n"
        "[dim]Your terminal UI is now beautiful and professional[/dim]",
        border_style="green",
        padding=(1, 2)
    ))
    console.print()

    print("\n✅ Rich library is installed and working perfectly!")
    print("🎨 All scripts will now display colorful output!")

except ImportError:
    print("\n❌ Rich library not installed!")
    print("📦 Install with: pip install rich")
    print("\nWithout rich, scripts will use plain text output (functionality unchanged)")

