"""Agent responsible for analyzing user queries and determining intent."""

import re
from typing import List

from core.router import IntentType, Intent
class Analyst:
    """Analyzes prompts to determine request type and complexity."""

    CODE_KEYWORDS = [
        "dockerfile", "docker", "code", "script", "fonction", "classe",
        "api", "endpoint", "routage", "microservice", "serveur",
        "backend", "frontend", "python", "javascript", "typescript",
        "java", "go", "rust", "sql", "query", "schema", "model",
        "class ", "def ", "import ", "from ", "return ", "if __name__",
    ]

    COMPLEX_KEYWORDS = [
        "compare", "vs", "difference", "pros and cons", "avantages",
        "inconvénients", "best practice", "architecture", "design",
        "scalability", "performance", "security", "authentication",
    ]

    def analyze(self, prompt: str) -> Intent:
        """Analyze prompt using keyword detection and length heuristics."""
        content = prompt.lower().strip()
        words = prompt.split()
        length = len(words)

        # Check for CODE intent
        code_score = sum(1 for kw in self.CODE_KEYWORDS if kw in content)
        if code_score >= 1:
            return Intent(type=IntentType.CODE, complexity=4)

        # Check for COMPLEX intent
        complex_score = sum(1 for kw in self.COMPLEX_KEYWORDS if kw in content)
        if length >= 30 or complex_score >= 2:
            return Intent(type=IntentType.COMPLEX, complexity=3)
        elif length >= 15:
            return Intent(type=IntentType.COMPLEX, complexity=2)
        else:
            return Intent(type=IntentType.SIMPLE, complexity=1)