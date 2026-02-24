from typing import Optional

from langchain_ollama import ChatOllama

from src.settings import settings


def create_ollama_client(tools: list = None) -> ChatOllama:
    client = ChatOllama(
        model=settings.MODEL_NAME,
        base_url=settings.OLLAMA_BASE_URL,
        client_kwargs={
            "headers": {"Authorization": f"Bearer {settings.OLLAMA_API_KEY}"}
        },
        temperature=0,
        timeout=30,
    )

    if tools is not None:
        client = client.bind_tools(tools)

    return client
