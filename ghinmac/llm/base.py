import asyncio
from typing import List, Dict, Any
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, allowed_tools: List[str] = None) -> Dict[str, Any]:
        """
        Returns a dict that either contains:
        {"action": "tool_call", "tool": "tool_name", "args": {...}}
        OR
        {"action": "reply", "content": "..."}
        """
        pass
