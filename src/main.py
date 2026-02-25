import asyncio
import argparse
import sys
from pathlib import Path

# Allow running as `python src/main.py` (not just `python -m src.main`)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.errors import GraphRecursionError
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.status import Status

from src.agents import smart_researcher
from src.state import EvaluationConstants

console = Console()

NODE_STYLES = {
    "researcher": ("bold cyan", "🔍"),
    "tools": ("bold yellow", "🔧"),
    "evaluator": ("bold magenta", "⚖️"),
    "search_limit_answer": ("bold green", "✨"),
}


def visualize_graph():
    try:
        image = smart_researcher.get_graph().draw_mermaid_png()
        with open("researcher_graph.png", "wb") as f:
            f.write(image)

    except Exception as e:
        console.print(f"[bold red]Error visualizing graph and generating image:[/] {e}")


def _extract_final_content(state: dict | None) -> str:
    """Safely extract the last message with content from the full graph state."""
    if not state or "messages" not in state:
        return "No result was produced."

    messages = state["messages"]

    if isinstance(messages, BaseMessage):
        return messages.content or "No result was produced."

    if isinstance(messages, list) and messages:
        for msg in reversed(messages):
            if isinstance(msg, BaseMessage) and msg.content:
                return msg.content

    return "No result was produced."


async def run_agent(user_query: str):
    initial_state = {
        "messages": [HumanMessage(content=user_query)],
        "search_count": 0,
        "evaluation_result": EvaluationConstants.PENDING,
        "feedback": "",
    }
    config = {
        "recursion_limit": 25,
        "run_name": f"research: {user_query[:50]}",
        "tags": ["research-agent", "interactive"],
        "metadata": {"query": user_query},
    }

    console.print()
    console.print(Panel(
        f"[bold]{user_query}[/]",
        title="[bold blue]Research Query[/]",
        border_style="blue",
    ))
    console.print()

    try:
        status = Status("[bold cyan]🔍 researcher agent :: work in progress ...[/]", console=console)
        status.start()
        try:
            final_state = await smart_researcher.ainvoke(initial_state, config)
        finally:
            status.stop()

        console.print()
        console.print(Rule("[bold green]Research Complete[/]", style="green"))
        console.print()

        content = _extract_final_content(final_state)
        console.print(Panel(
            Markdown(content),
            title="[bold green]Final Result[/]",
            border_style="green",
            padding=(1, 2),
        ))

    except GraphRecursionError:
        console.print(
            "\n[bold red]Recursion limit reached:[/] The agent exceeded the maximum number of steps. "
            "Try a more specific query."
        )
    except Exception as e:
        console.print(f"\n[bold red]Error:[/] [{type(e).__name__}] {e}")


def main():
    parser = argparse.ArgumentParser(description="Agentic Research Assistant")
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Visualize the researcher graph instead of running the agent",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="The research query to investigate",
    )

    args = parser.parse_args()

    if args.visualize:
        visualize_graph()
    else:
        if not args.query:
            user_query = console.input("[bold cyan]\nEnter your research query:[/] ").strip()
            if not user_query:
                console.print("[bold red]Error:[/] Query cannot be empty")
                sys.exit(1)
        else:
            user_query = args.query

        asyncio.run(run_agent(user_query))


if __name__ == "__main__":
    main()
