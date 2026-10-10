import asyncio
from .base import LLMProvider

class MockProvider(LLMProvider):
    async def generate(self, prompt: str, allowed_tools=None) -> dict:
        await asyncio.sleep(0.5) # Simulate latency
        
        # Super simple rule-based mock for testing
        if "order" in prompt.lower() and "validate_order" in (allowed_tools or []):
            return {"action": "tool_call", "tool": "validate_order", "args": {"order_id": "123"}}
        elif "stock" in prompt.lower() and "check_stock" in (allowed_tools or []):
             return {"action": "tool_call", "tool": "check_stock", "args": {"item_id": "ABC"}}
        else:
            return {"action": "reply", "content": "Done processing task."}
