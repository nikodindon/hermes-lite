"""Main CLI interface for interacting with the Hermes Lite system."""

import asyncio
import sys
from typing import List

from agents.analyst import Analyst
from agents.critic import Critic
from core.aggregator import Aggregator
from core.router import Router
from core.orchestrator import Orchestrator
from core.benchmark import Benchmark
from core.benchmark_formatter import BenchmarkFormatter
from rich.console import Console
from utils.logger import get_logger

logger = get_logger()

async def main():
    console = Console()

    # Initialize components
    analyst = Analyst()
    critic = Critic()
    router = Router()
    orchestrator = Orchestrator()
    aggregator = Aggregator()
    benchmark = Benchmark(critic)
    formatter = BenchmarkFormatter()

    # Simple CLI loop
    console.print("[bold cyan]Hermes Lite v0.1[/bold cyan]")
    console.print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            prompt = input("> ").strip()
            if prompt.lower() in ("exit", "quit"):
                break
            if not prompt:
                continue

            logger.info(f"\\n=== Hermes Lite Query ===\\nPrompt: {prompt}")

            # 1. Analyze intent
            intent = analyst.analyze(prompt)
            logger.debug(f"Intent analysis: {intent}")

            # 2. Select models based on intent
            selected_models = router.select(intent)
            logger.info(f"Selected models: {selected_models}")

            # 3. Run async calls with benchmarking
            benchmark = Benchmark(critic)
            for model in selected_models:
                benchmark.start_timer(model)

            async with Orchestrator() as orchestrator:
                responses = await orchestrator.run(selected_models, prompt)

            for model, response in zip(selected_models, responses):
                benchmark.end_timer(model, response)

            # 4. Merge responses
            final_response = aggregator.merge(responses)
            logger.info(f"\\n--- Merged Response ---\\n{final_response.get('content', 'No content')[:200]}...")

            # 5. Show benchmark
            metrics = benchmark.get_metrics()
            formatter.show_comparison(metrics)

        except KeyboardInterrupt:
            console.print("\\n[red]Interrupted. Type 'exit' to quit.[/red]")
            continue
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            console.print(f"\\n[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\\n[red]Goodbye![/red]")