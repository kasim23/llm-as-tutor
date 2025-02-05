from ..utils.config import settings
import openai

def get_answer(question: str) -> str:
    openai.api_key = settings.OPENAI_API_KEY
    # Implement your LLM logic here. For demonstration, returning a placeholder.
    response = f"Echoing your question: {question}"
    return response
