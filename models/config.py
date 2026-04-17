"""Configuration for free OpenRouter models."""

from __future__ import annotations

# List of free OpenRouter model identifiers
FREE_MODELS = [
    "meta-llama/llama-3-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-7b-it:free",
]

# Default selection strategy parameters
DEFAULT_COUNT = 2  # number of models to use for parallel calls
DEFAULT_TIMEOUT = 30  # seconds per request
