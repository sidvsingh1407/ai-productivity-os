import google.generativeai as genai
import os
import asyncio
import itertools
import logging
from config import settings

logger = logging.getLogger(__name__)

class GeminiClientManager:
    """
    Round-robin load balancer across two Gemini API keys.
    On rate limit or API error from one key, automatically
    retries with the other key before falling back to static narrative.
    """

    def __init__(self):
        self.keys = [
            k for k in [
                settings.GEMINI_API_KEY1 or os.environ.get("GEMINI_API_KEY1"),
                settings.GEMINI_API_KEY2 or os.environ.get("GEMINI_API_KEY2"),
            ] if k
        ]
        if not self.keys:
            logger.warning("No Gemini API keys configured.")
        self._counter = itertools.cycle(range(len(self.keys))) if self.keys else None

    def _get_next_key(self) -> str | None:
        if not self.keys:
            return None
        return self.keys[next(self._counter)]

    async def generate(self, prompt: str) -> str | None:
        """
        Try each available key in round-robin order.
        Returns the text response or None if all keys fail.
        """
        attempted = set()
        while len(attempted) < len(self.keys):
            key = self._get_next_key()
            if not key or key in attempted:
                if len(attempted) == len(self.keys):
                    break
                # If we've seen it but haven't exhausted all, get next.
                # This ensures we don't prematurely break due to concurrent counter advances
                continue
            attempted.add(key)
            try:
                # Note: genai.configure sets global state, which can be subject to race conditions
                # but is the standard way to configure the genai module.
                genai.configure(api_key=key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = await asyncio.to_thread(
                    model.generate_content,
                    prompt,
                    generation_config={"temperature": 0, "max_output_tokens": 2048}
                )
                return response.text
            except Exception as e:
                logger.warning(f"Gemini key attempt failed: {type(e).__name__}: {e}. Trying next key.")
                continue
        logger.error("All Gemini API keys failed. Falling back to static narrative.")
        return None

# Singleton instance
gemini_manager = GeminiClientManager()
