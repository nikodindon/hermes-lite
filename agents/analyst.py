"""Agent responsible for analyzing user queries and determining their intent type/complexity."""

from dataclasses import dataclass
from core.router import IntentType, Intent

class Analyst:
    """Analyzes prompts to determine request type and complexity."""

    def analyze(self, prompt: str) -> Intent:
        """Basic analysis based on prompt length and content."""
        words = prompt.split()
        length = len(words)
        content = prompt.lower()
        
        if "code" in content or "script" in content:
            return Intent(type=IntentType.CODE, complexity=4)
        elif length < 10:
            return Intent(type=IntentType.SIMPLE, complexity=1)
        elif length < 30:
            return Intent(type=IntentType.COMPLEX, complexity=2)
        else:
            return Intent(type=IntentType.COMPLEX, complexity=3)  # May need expert analysis
