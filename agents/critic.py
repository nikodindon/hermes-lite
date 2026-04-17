"""Agent that evaluates and scores responses from different models."""

from typing import Dict, Any

class Critic:
    """Scores responses on various criteria."""

    def score_response(self, response: Dict[str, Any]) -> Dict[str, float]:
        """Return multiple scores for the response."""
        score = 0.0
        details = {}

        # Metrics (simple placeholders)
        choices = response.get("choices", [])
        if choices:
            choice = choices[0]
            message = choice.get("message", {})
            content = message.get("content", "")
            usage = choice.get("usage", {})
            tokens = usage.get("total_tokens", 0)

            # Simple scoring heuristics
            length = len(content)
            score = min(1.0, length / 50)  # Reward moderate length
            score = max(0.0, score - 0.1)  # Slight penalty

            details["len"] = length
            details["token_count"] = tokens
            details["score"] = score

        return details