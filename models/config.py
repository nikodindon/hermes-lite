"""Configuration for free OpenRouter models (updated April 2026)."""

from __future__ import annotations

# List of free OpenRouter model identifiers as of April 2026.
# Prefer models known for stability and coding/general quality.
FREE_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",      # Excellent reasoning
    "qwen/qwen3-coder:free",                       # Best for code
    "google/gemma-4-31b-it:free",                  # Very good generalist
    "google/gemma-4-26b-a4b-it:free",              # Good generalist
    "qwen/qwen3-next-80b-a3b-instruct:free",       # Good coding/reasoning
]

# Default selection strategy parameters
DEFAULT_COUNT = 3          # number of models to use for parallel calls
DEFAULT_TIMEOUT = 30       # seconds per request
DEFAULT_MAX_TOKENS = 512
