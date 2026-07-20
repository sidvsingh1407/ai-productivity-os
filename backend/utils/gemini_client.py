import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_DIMENSION = 768

GEMINI_API_KEYS = [
    os.environ.get("GEMINI_API_KEY1"),
    os.environ.get("GEMINI_API_KEY2"),
]

def get_gemini_response(prompt: str, model: str = "gemini-1.5-pro") -> str:
    """
    Attempt to get a Gemini response using available API keys.
    Falls back to the second key if the first hits a quota/rate limit error.
    Returns the generated text or raises if both keys fail.
    """
    last_error = None
    for i, key in enumerate(GEMINI_API_KEYS):
        if not key:
            continue
        try:
            genai.configure(api_key=key)
            model_client = genai.GenerativeModel(model)
            response = model_client.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.warning(f"Gemini key {i+1} failed: {str(e)}")
            last_error = e
            continue
    raise RuntimeError(f"All Gemini API keys exhausted. Last error: {last_error}")

def embed_text(text: str) -> list[float]:
    """
    Attempt to get an embedding for the provided text using available API keys.
    Falls back to the second key if the first hits a quota/rate limit error.
    Returns the embedding vector (list of floats) or raises if both keys fail.
    """
    last_error = None
    for i, key in enumerate(GEMINI_API_KEYS):
        if not key:
            continue
        try:
            genai.configure(api_key=key)
            result = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.warning(f"Gemini key {i+1} failed for embedding: {str(e)}")
            last_error = e
            continue
    raise RuntimeError(f"All Gemini API keys exhausted for embedding. Last error: {last_error}")
