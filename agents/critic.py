"""Agent that evaluates and scores responses from different models."""

import re
from typing import Dict, Any, List

class Critic:
    """Scores responses on clarity, precision, and hallucination detection."""

    def __init__(self):
        # Keywords that often indicate hallucination or lack of grounding
        self.unsupported_markers = [
            r"\b(guess|assume|probably|maybe|seems like|likely)\b",
            r"\b(as an AI|I cannot verify|no source|unverified)\b",
        ]
        self.hallucination_penalty = 0.3

    def score_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return detailed scores for the response.
        Scores are in range [0.0, 1.0].
        """
        details: Dict[str, Any] = {"scores": {}}

        # Handle error responses transparently
        choices = response.get("choices", [])
        if not choices:
            details["scores"] = {"clarity": 0.0, "precision": 0.0, "hallucination": 0.0, "overall": 0.0}
            details["score"] = 0.0
            return details

        choice = choices[0]
        message = choice.get("message", {})
        content = message.get("content", "") or ""
        usage = choice.get("usage", {})
        tokens = usage.get("total_tokens", 0)
        latency = response.get("duration", 0.0)

        # 1) Clarity: sentence structure, punctuation, readability
        clarity = self._score_clarity(content)

        # 2) Precision: specificity, concrete details, numbers
        precision = self._score_precision(content)

        # 3) Hallucination detection
        hallucination_score = self._detect_hallucination(content)

        # Overall weighted score
        overall = (0.4 * clarity) + (0.4 * precision) + (0.2 * (1.0 - hallucination_score))
        overall = max(0.0, min(1.0, overall))

        details["scores"] = {
            "clarity": round(clarity, 3),
            "precision": round(precision, 3),
            "hallucination": round(hallucination_score, 3),
            "overall": round(overall, 3)
        }
        details["latency"] = latency
        details["tokens"] = tokens
        details["content_preview"] = content[:120]
        details["score"] = overall

        return details

    def _score_clarity(self, text: str) -> float:
        """Score based on sentence completeness and grammar cues."""
        if not text.strip():
            return 0.0
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0.5
        # Simple heuristic: longer, structured text => clearer
        score = min(1.0, len(sentences) / 3.0)
        # Bonus for punctuation consistency
        if "." in text and (text.count(".") >= text.count("?")):
            score += 0.05
        return min(1.0, score)

    def _score_precision(self, text: str) -> float:
        """Score based on concrete terms, numbers, and specificity."""
        if not text.strip():
            return 0.0
        # Look for numbers, named entities, specific terms
        has_numbers = bool(re.search(r"\b\d+\b", text))
        # Count capitalized nouns/start-of-sentence words as potential entities
        words = text.split()
        capitalized = sum(1 for w in words if w[0:1].isupper())
        score = 0.3 + (0.4 if has_numbers else 0.0) + min(0.3, capitalized / 10.0)
        return min(1.0, score)

    def _detect_hallucination(self, text: str) -> float:
        """Return a score [0,1] indicating likelihood of hallucination."""
        if not text.strip():
            return 0.0
        text_lower = text.lower()
        score = 0.0
        for pattern in self.unsupported_markers:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += self.hallucination_penalty
        return min(1.0, score)