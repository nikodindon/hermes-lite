"""Synthesizer agent that produces final answer from model responses."""

from typing import List, Dict, Any

class Synthesizer:
    """Combine responses and scores into a final answer."""

    def synthesize(self, responses: List[Dict[str, Any]], scores: List[float]) -> Dict[str, Any]:
        """
        Merge best responses and provide a short, grounded justification.
        responses: list of model response dicts (may include error responses)
        scores: list of numeric scores aligned with responses
        """
        if not responses:
            return {"content": "No valid responses.", "justification": "No models returned usable output."}

        # Filter out error-only responses
        valid = []
        valid_scores = []
        for r, s in zip(responses, scores):
            choices = r.get("choices", [])
            if choices and choices[0].get("message", {}).get("content"):
                valid.append(r)
                valid_scores.append(s)

        if not valid:
            # All had errors; return first response with error note
            first = responses[0] if responses else {}
            content = first.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {
                "content": content or "Unable to generate a response (all models errored).",
                "justification": "No models produced valid output; see comparison for error details.",
                "selected_model": first.get("model", "unknown"),
                "score": 0.0,
                "errors_present": True
            }

        # Pick the highest-scoring valid response
        best_idx = valid_scores.index(max(valid_scores))
        best = valid[best_idx]
        content = best.get("choices", [{}])[0].get("message", {}).get("content", "")
        model = best.get("model", "unknown")
        score = valid_scores[best_idx]

        # Lightweight justification: mention key factors
        clarity = best.get("scores", {}).get("clarity", 0.0)
        precision = best.get("scores", {}).get("precision", 0.0)
        hallucination = best.get("scores", {}).get("hallucination", 0.0)

        justification = (
            f"Selected '{model}' (overall: {score:.2f}, clarity: {clarity:.2f}, "
            f"precision: {precision:.2f}, hallucination risk: {hallucination:.2f}). "
            "For critical use cases, verify facts against authoritative sources."
        )

        return {
            "content": content,
            "justification": justification,
            "selected_model": model,
            "score": score,
            "errors_present": False
        }