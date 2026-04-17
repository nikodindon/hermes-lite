"""Merge multiple model responses into a single final answer."""

from typing import List, Dict, Any
from agents.critic import Critic
from agents.synthesizer import Synthesizer
from utils.metrics import build_summary_entry

class Aggregator:
    """Combine responses, score them, and synthesize a final answer."""

    def __init__(self):
        self.critic = Critic()
        self.synthesizer = Synthesizer()

    def merge(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Score all responses, then synthesize a final answer.
        Keeps error responses for transparency in benchmarking.
        """
        if not responses:
            return {"content": "No valid responses received."}

        # Score each response
        scores = []
        valid_responses = []
        for resp in responses:
            details = self.critic.score_response(resp)
            score = details.get("score", 0.0)
            scores.append(score)
            valid_responses.append(resp)

        # Synthesize from valid responses
        synthesis = self.synthesizer.synthesize(valid_responses, scores)

        # Augment with a concise comparison summary for the user
        summary_entries = [build_summary_entry(r, r.get("model", "unknown")) for r in valid_responses]
        synthesis["comparison"] = summary_entries

        return synthesis

    def format_comparison(self, metrics_list: List[Dict[str, Any]]) -> str:
        """Produce a simple comparison table string for CLI display."""
        lines = ["Model                 Latency   Score   Tokens"]
        lines.append("-------------------------------------------")
        for m in metrics_list:
            lines.append(f"{m['model'][:20]:20} {m['latency']:>8.2f} {m['score']:>6.1f} {m['tokens']:>6}")
        return "\n".join(lines)