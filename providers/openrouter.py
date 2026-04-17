"""OpenRouter API wrapper for calling free models."""

import os
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

class OpenRouterProvider:
    """Wrapper for OpenRouter API calls."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hermes-lite.local",  # Optional but recommended
            "X-Title": "Hermes Lite",  # Optional but recommended
        }
    
    async def call_model(self, model: str, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Call a specific model via OpenRouter API.
        
        Args:
            model: Model identifier (e.g., "meta-llama/llama-3-8b-instruct:free")
            prompt: User prompt to send
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary containing response data
        """
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
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
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": str(e),
                    "response": e.response.text if e.response else None
                }
            except Exception as e:
                return {
                    "error": True,
                    "message": f"Unexpected error: {str(e)}"
                }

# Convenience function for synchronous-like usage (will be adapted for async)
def create_provider() -> OpenRouterProvider:
    """Factory function to create an OpenRouter provider instance."""
    return OpenRouterProvider()