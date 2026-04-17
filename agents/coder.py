"""Dedicated code generation agent for CODE intents."""

from typing import List, Dict, Any

from core.router import IntentType
from agents.critic import Critic
class Coder:
    """Generates code with a specialized prompt when intent is CODE."""

    def __init__(self):
        self.critic = Critic()

    def generate(self, user_prompt: str, model: str) -> Dict[str, Any]:
        """Build a code-focused prompt and call the model.
        Returns the raw OpenRouter response.
        """
        code_prompt = (
            "You are an expert DevOps and Python engineer. "
            "Write clean, production-ready code focused on the task. "
            "Include a short explanation, error handling where relevant, "
            "and example usage.\n\n"
            f"Task: {user_prompt}"
        )
        # Note: actual model call is handled by orchestrator/aggregator.
        # This agent prepares the prompt; the caller executes the API request.
        return {"prompt": code_prompt, "model": model}

    def refine_response(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """Score and optionally improve a code response."""
        details = self.critic.score_response(raw_response)
        raw_response["_coder_score"] = details.get("score", 0.0)
        raw_response["_coder_details"] = details
        return raw_response