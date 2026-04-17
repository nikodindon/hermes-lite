"""OpenRouter API wrapper for calling free models."""

import os
import sys
import time
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    print("[ERROR] OPENROUTER_API_KEY environment variable is not set.")
    print("Create a .env file with: OPENROUTER_API_KEY=your_key_here")
    sys.exit(1)

class OpenRouterProvider:
    """Wrapper for OpenRouter API calls."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hermes-lite.local",
            "X-Title": "Hermes Lite",
        }

    async def call_model(self, model: str, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """Call a specific model via OpenRouter API."""
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            }
            try:
                response = await client.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                if response.status_code == 429:
                    return {
                        "error": True,
                        "status_code": 429,
                        "message": "[Rate limit] OpenRouter free est temporairement saturé. Réessaie dans 1-2 minutes.",
                    }
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": str(e),
                    "response": e.response.text if e.response else None,
                }
            except Exception as e:
                return {
                    "error": True,
                    "message": f"Unexpected error: {str(e)}"
                }

def create_provider() -> OpenRouterProvider:
    """Factory function to create an OpenRouter provider instance."""
    return OpenRouterProvider()