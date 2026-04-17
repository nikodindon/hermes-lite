"""Coordinator for parallel model requests using asyncio."""

import asyncio
from typing import List, Dict, Any
from providers.openrouter import OpenRouterProvider
from models.config import DEFAULT_COUNT, DEFAULT_TIMEOUT, DEFAULT_MAX_TOKENS

class Orchestrator:
    """Manage concurrent requests to multiple models."""

    def __init__(self):
        self.provider = OpenRouterProvider()
        self.semaphore = asyncio.Semaphore(DEFAULT_COUNT)

    async def run(self, models: List[str], prompt: str) -> List[Dict[str, Any]]:
        """Execute parallel calls and return responses, including error responses for benchmarking."""
        # Limit models to DEFAULT_COUNT even if router returned more
        limited = models[:DEFAULT_COUNT]
        responses = []
        for i, model in enumerate(limited):
            async with self.semaphore:
                task = asyncio.create_task(
                    self.provider.call_model(
                        model=model,
                        prompt=prompt,
                        max_tokens=DEFAULT_MAX_TOKENS,
                        timeout=DEFAULT_TIMEOUT,
                    )
                )
                responses.append(await task)
            # Be gentle with rate limits between calls
            if i < len(limited) - 1:
                await asyncio.sleep(0.4)
            # Keep all responses (including errors) so benchmark can compare failure modes
            return responses

# Usage example
# orch = Orchestrator()
# responses = await orch.run(FREE_MODELS[:2], "Test query")