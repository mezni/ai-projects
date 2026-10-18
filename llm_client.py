from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import settings

# Newer reasoning models only accept the default temperature.
TEMP_UNSUPPORTED_PREFIXES = ("gpt-5", "gpt-6", "o1", "o3", "o4", "codex")


def get_llm(temperature: float = 0.2, streaming: bool = True):
    """Returns the configured ChatOpenAI instance."""
    if not settings.OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API key is missing. Set it in your .env file or sidebar."
        )
    kwargs = {
        "model": settings.MODEL_NAME,
        "openai_api_key": settings.OPENAI_API_KEY,
        "streaming": streaming,
    }
    if not settings.MODEL_NAME.startswith(TEMP_UNSUPPORTED_PREFIXES):
        kwargs["temperature"] = temperature
    return ChatOpenAI(**kwargs)


def get_embeddings():
    """Returns the configured OpenAIEmbeddings instance."""
    if not settings.OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API key is missing. Set it in your .env file or sidebar."
        )
    return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
