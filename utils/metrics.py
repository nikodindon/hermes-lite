"""Metrics collection helpers (latency, tokens, scoring)."""

from typing import Dict, Any

def extract_latency(response: Dict[str, Any]) -> float:
    """Extract timing info if present; otherwise 0.0."""
    # OpenRouter may include usage timings; this is a safe fallback.
    return float(response.get("duration", 0.0) or 0.0)

def estimate_tokens(content: str) -> int:
    """Rough token approximation for display purposes."""
    # Very rough: assume 4 chars per token.
    return max(1, len(content) // 4)

def build_summary_entry(response: Dict[str, Any], model: str) -> Dict[str, Any]:
    """Build a benchmark table row entry."""
    choices = response.get("choices", [])
    if not choices:
        return {"model": model, "latency": 0.0, "tokens": 0, "score": 0.0}
    choice = choices[0]
    usage = choice.get("usage", {})
    content = choice.get("message", {}).get("content", "")
    return {
        "model": model,
        "latency": extract_latency(response),
        "tokens": usage.get("total_tokens", estimate_tokens(content)),
        "score": float(choice.get("score", 0.0) or 0.0)
    }
