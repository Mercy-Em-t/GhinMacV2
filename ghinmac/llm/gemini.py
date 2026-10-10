import os
from .base import LLMProvider
from google import genai
from google.genai import types

class GeminiProvider(LLMProvider):
    def __init__(self):
        # Assumes GEMINI_API_KEY is in environment
        self.client = genai.Client()

    async def generate(self, prompt: str, allowed_tools=None) -> dict:
        # For Phase 1, we will just use basic text generation and simulate tool calls 
        # using structured prompting, or use the real tool calling API.
        # For simplicity in this mock, we will ask it to return JSON.
        sys_instruct = (
            "You are a corporate worker agent. You have tools you can use.\n"
            f"Allowed tools: {allowed_tools or []}\n"
            "You must respond in valid JSON format ONLY.\n"
            "Format: {\"action\": \"tool_call\", \"tool\": \"name\", \"args\": {}} OR {\"action\": \"reply\", \"content\": \"...\"}"
        )
        
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruct,
                response_mime_type="application/json",
            )
        )
        
        import json
        try:
            data = json.loads(response.text)
            return data
        except Exception as e:
            return {"action": "reply", "content": f"Error parsing LLM response: {str(e)}"}
