import re
import yaml
from pathlib import Path
from typing import Any, Dict
from functools import lru_cache

from .schemas.rag import ChatRequest

class RagHelper:
    @staticmethod
    @lru_cache(maxsize=1)
    def load_system_prompt() -> Dict[str, Any]:
        """Loads a system prompt from a YAML file."""
        from .config import settings
        file_path = settings.system_prompt_path

        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Configuration file not found at: {file_path}")

        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def prompt_template(query: ChatRequest) -> tuple:
        """Constructs a chat prompt template for the LLM."""
        default_system = RagHelper.load_system_prompt()

        # Check model in query and use default if not provided.
        model = query.model
        if isinstance(model, str):
            model = default_system["model"]

        question = query.question

        # Construct the messages list with system and user messages
        def system_prompt():
            return default_system['system_prompt']

        messages = [
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": question}
        ]

        return model, messages

    @staticmethod
    def parse_llm_response(response: Any, query: str) -> Dict[str, Any]:
        """Parses an LLM completion response into structured reasoning and final answer."""
        # Safely extract values whether response is an object or dict
        if isinstance(response, dict):
            choice = response.get("choices", [{}])[0]
            message = choice.get("message", {})
            response_text = message.get("content", "") or ""
            reasoning_role = message.get("role", "assistant")

            model = response.get("model", "")
            usage = response.get("usage", {})
            total_tokens = usage.get("total_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            prompt_tokens = usage.get("prompt_tokens", 0)
        else:
            choice = response.choices[0]
            message = choice.message
            response_text = getattr(message, "content", "") or ""
            reasoning_role = getattr(message, "role", "assistant")

            model = getattr(response, "model", "")
            usage = getattr(response, "usage", None)
            total_tokens = getattr(usage, "total_tokens", 0) if usage else 0
            completion_tokens = (
                getattr(usage, "completion_tokens", 0) if usage else 0
            )
            prompt_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0

        # Extract <think> content for reasoning
        pattern = r"<think>(.*?)</think>"
        think_match = re.search(pattern, response_text, re.DOTALL)
        reasoning = think_match.group(1).strip() if think_match else ""

        # Remove <think> tags from the main answer
        answer = re.sub(pattern, "", response_text, flags=re.DOTALL).strip()

        return {
            "model": model,
            "input_tokens": prompt_tokens,
            "output_tokens": completion_tokens,
            "completions": {
                "answer": answer,
                "reasoning": {"role": reasoning_role, "reason": reasoning},
            },
        }

