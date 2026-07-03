from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()


def title():
    console.print()
    console.print(
        Rule("[bold cyan]🤖 Multi Server MCP Agent[/bold cyan]")
    )


def loading():
    console.print(
        "[bold yellow]⏳ Loading MCP tools...[/bold yellow]"
    )


def loaded(num_tools: int):
    console.print(
        f"[bold green]✓ Loaded[/bold green] [cyan]{num_tools}[/cyan] tools\n"
    )


def ready():
    console.print(
        "[bold green]🚀 Ready![/bold green]"
    )
    console.print(
        "[dim]Type 'exit' or 'quit' to stop.[/dim]\n"
    )


def user():
    console.print(
        "[bold green]You[/bold green] > ",
        end=""
    )


def assistant():
    console.print()
    console.print("[bold cyan]Assistant[/bold cyan] > ", end="")


def tool_cli(name):
    console.print()
    console.print(
        f"[bold yellow]⚡[/bold yellow] "
        f"[cyan]{name}[/cyan]"
    )


def tool_done():
    console.print(
        "[green]✓ Finished[/green]"
    )


def error(message: str):
    console.print(
        f"[bold red]✗ {message}[/bold red]"
    )


def info(message: str):
    console.print(
        f"[blue]{message}[/blue]"
    )