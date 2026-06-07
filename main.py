import os
import sys
import pyperclip
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
from rich.text import Text

from sources.rss_feeds import fetch_rss_trends
from sources.web_scraper import fetch_scraped_trends
from sources.google_news import fetch_google_news_trends
from analyzer import analyze_trends
from post_generator import generate_posts

load_dotenv()
console = Console()


def collect_all_trends():
    console.print("\n[bold cyan]Fetching latest AI trends from multiple sources...[/bold cyan]\n")

    all_articles = []

    with console.status("[bold green]Fetching RSS feeds..."):
        rss = fetch_rss_trends()
        all_articles.extend(rss)
        console.print(f"  [green]✓[/green] RSS Feeds: {len(rss)} articles")

    with console.status("[bold green]Fetching Hacker News & Reddit..."):
        scraped = fetch_scraped_trends()
        all_articles.extend(scraped)
        console.print(f"  [green]✓[/green] Web Sources: {len(scraped)} articles")

    with console.status("[bold green]Fetching Google News..."):
        gnews = fetch_google_news_trends()
        all_articles.extend(gnews)
        console.print(f"  [green]✓[/green] Google News: {len(gnews)} articles")

    console.print(f"\n[bold]Total articles collected: {len(all_articles)}[/bold]")
    return all_articles


def display_topics(topics_data):
    topics = topics_data.get("topics", [])
    if not topics:
        console.print("[red]No topics found. Try again later.[/red]")
        return []

    table = Table(title="🔥 Top AI Trends Right Now", show_lines=True)
    table.add_column("#", style="bold cyan", width=4)
    table.add_column("Topic", style="bold white", max_width=40)
    table.add_column("Summary", max_width=50)
    table.add_column("Score", style="bold yellow", width=6, justify="center")

    for topic in topics:
        score = topic.get("post_worthiness", 0)
        score_color = "green" if score >= 7 else "yellow" if score >= 5 else "red"
        table.add_row(
            str(topic["id"]),
            topic["title"],
            topic["summary"][:100] + "..." if len(topic["summary"]) > 100 else topic["summary"],
            f"[{score_color}]{score}/10[/{score_color}]",
        )

    console.print()
    console.print(table)
    return topics


def display_posts(posts_data):
    posts = posts_data.get("posts", [])
    if not posts:
        console.print("[red]Failed to generate posts.[/red]")
        return []

    for post in posts:
        version = post.get("version", "?")
        angle = post.get("angle", "Unknown")

        console.print()
        console.print(
            Panel(
                post["post"],
                title=f"[bold cyan]Version {version}[/bold cyan] - [yellow]{angle}[/yellow]",
                border_style="cyan",
                padding=(1, 2),
            )
        )

    return posts


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print(
            Panel(
                "[red]GROQ_API_KEY not found![/red]\n\n"
                "1. Copy [cyan].env.example[/cyan] to [cyan].env[/cyan]\n"
                "2. Add your Groq API key\n"
                "3. Run again",
                title="Setup Required",
                border_style="red",
            )
        )
        sys.exit(1)

    console.print(
        Panel(
            "[bold cyan]LinkedIn Post Generator[/bold cyan]\n"
            "[dim]Fetch AI trends → Analyze → Generate posts in your style[/dim]",
            border_style="cyan",
        )
    )

    articles = collect_all_trends()

    if not articles:
        console.print("[red]No articles found. Check your internet connection.[/red]")
        sys.exit(1)

    with console.status("[bold green]Analyzing trends with AI..."):
        topics_data = analyze_trends(articles, api_key)

    topics = display_topics(topics_data)
    if not topics:
        sys.exit(1)

    while True:
        console.print()
        choice = Prompt.ask(
            "[bold]Select a topic number to generate posts (or 'q' to quit)",
            default="1",
        )

        if choice.lower() == "q":
            console.print("[dim]Bye![/dim]")
            break

        try:
            topic_idx = int(choice) - 1
            if topic_idx < 0 or topic_idx >= len(topics):
                console.print("[red]Invalid topic number.[/red]")
                continue
        except ValueError:
            console.print("[red]Enter a valid number.[/red]")
            continue

        selected_topic = topics[topic_idx]
        console.print(f"\n[bold green]Generating posts for:[/bold green] {selected_topic['title']}")

        with console.status("[bold green]Generating 4 post versions..."):
            posts_data = generate_posts(selected_topic, api_key)

        posts = display_posts(posts_data)
        if not posts:
            continue

        console.print()
        post_choice = Prompt.ask(
            "[bold]Pick a version to copy (1-4), 'r' to regenerate, 'b' to go back",
            default="1",
        )

        if post_choice.lower() == "r":
            console.print("[yellow]Regenerating...[/yellow]")
            with console.status("[bold green]Generating fresh versions..."):
                posts_data = generate_posts(selected_topic, api_key)
            posts = display_posts(posts_data)
            if not posts:
                continue
            post_choice = Prompt.ask(
                "[bold]Pick a version to copy (1-4)",
                default="1",
            )

        if post_choice.lower() == "b":
            continue

        try:
            post_idx = int(post_choice) - 1
            if 0 <= post_idx < len(posts):
                selected_post = posts[post_idx]["post"]
                try:
                    pyperclip.copy(selected_post)
                    console.print(
                        Panel(
                            "[bold green]Post copied to clipboard![/bold green]\n\n"
                            "Go to LinkedIn and paste it.",
                            border_style="green",
                        )
                    )
                except Exception:
                    console.print(
                        Panel(
                            selected_post,
                            title="[bold green]Your Post (copy manually)[/bold green]",
                            border_style="green",
                            padding=(1, 2),
                        )
                    )
            else:
                console.print("[red]Invalid version number.[/red]")
        except ValueError:
            console.print("[red]Enter a valid number.[/red]")

        another = Prompt.ask("\n[bold]Generate for another topic?[/bold]", choices=["y", "n"], default="y")
        if another == "n":
            console.print("[dim]Bye! Go post something great.[/dim]")
            break


if __name__ == "__main__":
    main()
