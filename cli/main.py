"""Main CLI interface for interacting with the Hermes Lite system."""

import argparse
import asyncio
import sys
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from agents.analyst import Analyst
from agents.critic import Critic
from agents.synthesizer import Synthesizer
from agents.__init__ import *
from core.aggregator import Aggregator
from core.router import Router
from core.orchestrator import Orchestrator
from core.benchmark import Benchmark
from core.benchmark_formatter import BenchmarkFormatter
from core.memory import Memory
from utils.logger import get_logger
from utils.metrics import build_summary_entry

logger = get_logger()

async def run_once(prompt: str, critic: Critic, router: Router, orchestrator: Orchestrator,
                   aggregator: Aggregator, synthesizer: Synthesizer, memory: Memory,
                   bench: bool) -> Optional[dict]:
    """Run a single query and return the synthesis result (or None on error)."""
    console = Console()

    # 1) Analyze intent
    intent = Analyst().analyze(prompt)
    # 2) Select models
    selected_models = router.select(intent)
    # Limit models to DEFAULT_COUNT even if router returns more
    from models.config import DEFAULT_COUNT
    selected_models = selected_models[:DEFAULT_COUNT]

    # 3) Benchmark & execute
    benchmark = Benchmark(critic)
    for model in selected_models:
        benchmark.start_timer(model)

    responses = await orchestrator.run(selected_models, prompt)
    for model, response in zip(selected_models, responses):
        benchmark.end_timer(model, response)

    # 4) Score & synthesize
    final_result = aggregator.merge(responses)

    # 5) Update memory on successful synthesis
    if not final_result.get("errors_present", True):
        memory.add_entry(prompt, final_result.get("selected_model", "unknown"),
                         final_result.get("score", 0.0))
        logger.info("[Mémoire mise à jour]")

    # 6) Display
    if bench:
        metrics = benchmark.get_metrics()
        console.print(benchmark_formatter.format_comparison(metrics))

    # Rich output panel
    content = final_result.get("content", "")
    justification = final_result.get("justification", "")
    panel_body = f"[bold]Réponse finale:[/bold]\n{content}"
    if justification:
        panel_body += f"\n\n[dim]{justification}[/dim]"

    console.print(Panel(panel_body, title="Hermes Lite", border_style="cyan"))
    return final_result


async def main():
    parser = argparse.ArgumentParser(description="Hermes Lite – Multi-Agent AI Router")
    parser.add_argument("prompt", nargs="?", help="User query (one-shot mode)")
    parser.add_argument("--bench", action="store_true",
                        help="Show benchmark table for models")
    args = parser.parse_args()

    console = Console()
    critic = Critic()
    synthesizer = Synthesizer()
    router = Router()
    orchestrator = Orchestrator()
    aggregator = Aggregator()
    memory = Memory()
    formatter = BenchmarkFormatter()

    # Show preferred model from memory (info only)
    try:
        pref = memory.get_preferred_model([])
        logger.info(f"Modèle préféré en mémoire : {pref}")
    except Exception:
        pass

    # One-shot mode
    if args.prompt:
        await run_once(args.prompt, critic, router, orchestrator, aggregator, synthesizer, memory, args.bench)
        return

    # Interactive loop
    console.print("[bold cyan]Hermes Lite v0.1[/bold cyan]")
    console.print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            prompt_input = input("> ").strip()
            if prompt_input.lower() in ("exit", "quit"):
                break
            if not prompt_input:
                continue
            await run_once(prompt_input, critic, router, orchestrator, aggregator, synthesizer, memory, args.bench)
        except KeyboardInterrupt:
            console.print("\n[red]Interrupted. Type 'exit' to quit.[/red]")
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            console.print(f"\n[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[red]Goodbye![/red]")