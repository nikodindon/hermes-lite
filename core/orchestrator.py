"""Coordinator for parallel model requests using asyncio."""

import asyncio
from typing import List, Dict
from providers.openrouter import OpenRouterProvider
from models.config import DEFAULT_COUNT, DEFAULT_TIMEOUT

class Orchestrator:
    """Manage concurrent requests to multiple models."""

    def __init__(self, model_provider: OpenRouterProvider = None):
        self.provider = model_provider or OpenRouterProvider.create_provider()
        self.semaphore = asyncio.Semaphore(DEFAULT_COUNT)  # Limit concurrent calls

    async def run(self, models: List[str], prompt: str) -> List[Dict[str, any]]:
        """Execute parallel calls and return responses."""
        async with self.semaphore:
            tasks = []
            for model in models:
                task = asyncio.create_task(
                    self.provider.call_model(
                        model=model,
                        prompt=prompt,
                        max_tokens=512,  # Smaller for comparison
                        timeout=DEFAULT_TIMEOUT
                    )
                )
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return [r for r in responses if not r.get("error")]

# Usage example
# orch = Orchestrator()
# responses = await orch.run(FREE_MODELS[:2], "Test query")