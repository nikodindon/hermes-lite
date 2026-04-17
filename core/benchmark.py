"""Module de benchmark avec intégration du critèration."""

from typing import List, Dict, Any
import time
from agents.critic import Critic

class Benchmark:
    """Collecte et analyse des métriques avec critèrique."""

    def __init__(self, critic: Critic = None):
        self.critic = critic or Critic()
        self.metrics = {}

    def start_timer(self, model: str):
        """Démarre un chronomètre pour un modèle."""
        self.metrics[model] = {
            "start_time": time.time(),
            "latency": 0.0,
            "tokens": 0,
            "error": None,
            "score": 0.0
        }

    def end_timer(self, model: str, response: Dict[str, Any]):
        """Arrêt le chronomètre et calcule les métriques."""
        if model not in self.metrics:
            return

        metrics = self.metrics[model]
        metrics["end_time"] = time.time()
        metrics["latency"] = metrics["end_time"] - metrics["start_time"]

        # Extraction des tokens
        if "usage" in response:
            usage = response["usage"]
            metrics["tokens"] = usage.get("total_tokens", 0)
        else:
            metrics["tokens"] = 0

        # Scoring avec le critèque
        if "choices" in response:
            for choice in response["choices"]:
                if "message" in choice:
                    content = choice["message"].get("content", "")
                    # Appliquer le critèque pour le scoring
                    score_data = self.critic.score_response(response)
                    metrics["score"] = score_data.get("score", 0.0)

    def get_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques calculées."""
        return {
            "models": {model: {k: v for k, v in m.items() if k != "start_time"} for model, m in self.metrics.items()}
        }