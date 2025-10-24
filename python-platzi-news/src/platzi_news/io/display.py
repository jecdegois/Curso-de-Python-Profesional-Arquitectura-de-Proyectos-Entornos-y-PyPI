"""Display utilities for Platzi News."""

from rich.console import Console

from ..core.models import Article

console = Console()


def display_articles(articles: list[Article]) -> None:
    """Display articles in vertical format."""
    if not articles:
        console.print("[yellow]No se encontraron artículos.[/yellow]")
        return

    console.print("[bold blue]Artículos de Noticias:[/bold blue]\n")

    for i, article in enumerate(articles, 1):
        console.print(f"[bold cyan]Artículo {i}:[/bold cyan]")
        console.print(f"[bold]Título:[/bold] {article.title}")
        console.print(
            f"[bold]Descripción:[/bold] {article.description or 'Sin descripción'}"
        )
        console.print(f"[bold]URL:[/bold] {article.url}")
        console.print("─" * 50)
        console.print()


def display_answer(answer: str) -> None:
    """Display the AI answer."""
    console.print(f"\n[bold green]Respuesta:[/bold green] {answer}\n")


def display_error(message: str) -> None:
    """Display an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")
