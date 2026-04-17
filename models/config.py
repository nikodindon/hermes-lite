"""Configuration for free OpenRouter models (updated for 2026)."""

from __future__ import annotations

# List of free OpenRouter model identifiers as of April 2026.
# Prefer models known for cost efficiency and availability.
FREE_MODELS = [
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "qwen/qwen3-coder:free",
    "meta-llama/llama-4-scout:free",
    "meta-llama/llama-4-maverick:free",
    "mistralai/devstral-2-2512:free",
]

# Default selection strategy parameters
DEFAULT_COUNT = 3  # number of models to use for parallel calls
DEFAULT_TIMEOUT = 30  # seconds per request
DEFAULT_MAX_TOKENS = 512
