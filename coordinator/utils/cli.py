from rich.rule import Rule
from rich.panel import Panel
from rich.console import Console
from rich.syntax import Syntax

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


def agent_loaded(card):
    skills = "\n".join(f"• {s.name}" for s in card.skills)

    console.print(
        Panel.fit(
            f"[bold cyan]{card.name}[/bold cyan]\n"
            f"{card.description}\n\n"
            f"[bold]Skills[/bold]\n{skills}",
            title="✅ Agent Connected",
            border_style="green",
        )
    )


def planner_output(content):
    syntax = Syntax(content, "json", theme="monokai")
    console.print(
        Panel(
            syntax,
            title="🧠 Planner",
            border_style="cyan",
        )
    )

def running_step(agent, task):
    console.print(
        Panel.fit(
            f"[cyan]{agent}[/cyan]\n\n{task}",
            title="⚡ Executing",
            border_style="yellow",
        )
    )

def agent_result(agent, result):
    console.print(
        Panel(
            result,
            title=f"✅ {agent}",
            border_style="green"
        )
    )

def final(final_text):
    console.print(
    Panel(
        final_text,
        title="🤖 Final Answer",
        border_style="cyan"
    )
)
    

def normalize_result(result):
    if isinstance(result, list):
        texts = []

        for part in result:
            if isinstance(part, dict):
                texts.append(part.get("text", ""))

        return "\n".join(texts)

    return str(result)