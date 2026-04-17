"""Simple persistent memory for the Hermes Lite system."""

import json
import os
from typing import Dict, Any, List

from utils.logger import get_logger

logger = get_logger()

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "memory.json")

class Memory:
    """Lightweight memory: stores prompt -> best model -> score per interaction."""

    def __init__(self, path: str = MEMORY_PATH):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                logger.warning("Could not read memory file, starting fresh.")
        return {"history": []}

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except OSError as e:
            logger.error(f"Failed to save memory: {e}")

    def add_entry(self, prompt: str, best_model: str, score: float):
        self.data.setdefault("history", []).append({
            "prompt": prompt,
            "best_model": best_model,
            "score": score
        })
        self.save()

    def get_history(self) -> List[Dict[str, Any]]:
        return self.data.get("history", [])

    def get_preferred_model(self, default_models: List[str]) -> str:
        """
        Suggest a preferred model based on past history.
        If one model consistently scored higher, prefer it.
        """
        history = self.get_history()
        if not history:
            return default_models[0]
        # Count average score per model (score stored per entry)
        scores: Dict[str, List[float]] = {}
        for entry in history:
            model = entry.get("best_model", "")
            scores.setdefault(model, []).append(entry.get("score", 0.0))
        if not scores:
            return default_models[0]
        avg = {m: sum(ss)/len(ss) for m, ss in scores.items()}
        return max(avg, key=avg.get)
