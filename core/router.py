""Core router to choose which OpenRouter models to call based on intent."""

import logging
from dataclasses import dataclass
from typing import List

from models.config import FREE_MODELS, DEFAULT_COUNT
from core.memory import Memory

logger = logging.getLogger(__name__)

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
    """Select models for a given intent, with memory-aware prioritization."""

    def __init__(self, models: List[str] | None = None, count: int | None = None):
        self.models = models or FREE_MODELS
        self.count = count or DEFAULT_COUNT
        self.memory = Memory()

    def select(self, intent: Intent) -> List[str]:
        """Return a list of model identifiers to request.

        Priority:
        1) If a preferred model from memory is valid for the intent, put it first.
        2) Then fill remaining slots with the free models list (up to count).
        """
        preferred = self.memory.get_preferred_model(self.models)
        selected = []
        if preferred in self.models:
            selected.append(preferred)
            logger.debug(f"Router: preferred model from memory -> {preferred}")

        # Fill remaining slots with other free models, avoiding duplicates
        for model in self.models:
            if len(selected) >= min(self.count, len(self.models)):
                break
            if model not in selected:
                selected.append(model)

        logger.info(f"Router: selected models={selected} for intent={intent.type}")
        return selected

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