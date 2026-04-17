"""Core router to choose which OpenRouter models to call based on intent."""

from dataclasses import dataclass
from typing import List, Tuple

from models.config import FREE_MODELS, DEFAULT_COUNT

# Simple intent types
class IntentType(str):
    SIMPLE = "simple"
    COMPLEX = "complex"
    CODE = "code"
    UNKNOWN = "unknown"

@dataclass
class Intent:
    type: IntentType
    complexity: int  # 1-5 scale

class Router:
    """Select models for a given intent using the free model list."""

    def __init__(self, models: List[str] | None = None, count: int | None = None):
        self.models = models or FREE_MODELS
        self.count = count or DEFAULT_COUNT

    def select(self, intent: Intent) -> List[str]:
        """Return a list of model identifiers to request.

        For SIMPLE intents, use the first model. For COMPLEX, take the top `count` models.
        """
        if intent.type == IntentType.SIMPLE:
            return [self.models[0]]
        # For COMPLEX or unknown, use the configured number of models
        return self.models[: min(self.count, len(self.models))]

# Simple heuristic to determine intent from prompt length

def analyze_prompt(prompt: str) -> Intent:
    words = prompt.split()
    length = len(words)
    if length < 10:
        return Intent(type=IntentType.SIMPLE, complexity=1)
    elif length < 30:
        return Intent(type=IntentType.COMPLEX, complexity=2)
    else:
        return Intent(type=IntentType.COMPLEX, complexity=3)
