from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from pydantic.v1 import SecretStr


def create_llm(
    provider: Literal["ollama", "openai"],
    api_key: SecretStr,
    base_url: str,
    model: str,
    temperature: float,
) -> BaseChatModel:
    if provider == "openai":
        return ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=temperature,
        )
    elif provider == "ollama":
        client_kwargs = {}
        api_key_value = api_key.get_secret_value()
        if api_key_value and api_key_value != "ollama":
            client_kwargs["headers"] = {"Authorization": f"Bearer {api_key_value}"}

        return ChatOllama(
            base_url=base_url,
            model=model,
            temperature=temperature,
            client_kwargs=client_kwargs or None,
        )

    raise ValueError("Unknown provider")