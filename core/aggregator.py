"""Merge multiple model responses into a single final answer."""

from typing import List, Dict, Any

class Aggregator:
    """Combine and rank responses from multiple models."""

    def merge(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best response based on simple heuristics."""
        if not responses:
            return {"content": "No valid responses received."}
        if len(responses) == 1:
            return responses[0]

        # Heuristic: choose response with median length to avoid extremes
        lengths = [(r.get("choices", [{}])[0].get("message", {}).get("content", "")) for r in responses]
        lengths = [len(text) for text in lengths if isinstance(text, str)]
        if lengths:
            median_idx = sorted(range(len(lengths)), key=lambda i: lengths[i])[len(lengths)//2]
            return responses[median_idx]
        else:
            # Fallback to first response
            return responses[0]

    def format_comparison(self, responses: List[Dict[str, Any]]) -> str:
        """Produce a simple comparison for benchmarking."""
        lines = []
        for i, resp in enumerate(responses):
            model = resp.get("model", f"model_{i}")
            content = resp.get("choices", [{}])[0].get("message", {}).get("content", "")
            latency = resp.get("usage", {}).get("total_time", 0)  # placeholder
            lines.append(f"{model}: {len(content)} chars, ~{latency}s")
        return "\n".join(lines)