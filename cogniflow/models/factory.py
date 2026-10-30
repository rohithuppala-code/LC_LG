"""Universal Model Factory for instantiating LangChain chat models."""

from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from cogniflow.config.settings import get_settings


class ModelFactory:
    """Factory to instantiate and configure chat models uniformly across providers."""

    @staticmethod
    def create_model(
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        streaming: bool = True,
        **kwargs,
    ) -> BaseChatModel:
        """Instantiate a chat model based on the selected provider.

        Args:
            provider: 'google', 'openai', or 'groq'. If None, uses DEFAULT_LLM_PROVIDER.
            model_name: Specific model ID. If None, uses default for that provider.
            temperature: Sampling temperature (0.0 to 1.0).
            streaming: Whether to support token streaming.
            **kwargs: Extra arguments passed to the underlying model constructor.

        Returns:
            An instance of BaseChatModel.
        """
        settings = get_settings()
        selected_provider = (provider or settings.default_provider).lower()
        settings.validate_provider_key(selected_provider)

        if selected_provider == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI

            name = model_name or settings.google_default_model
            return ChatGoogleGenerativeAI(
                model=name,
                google_api_key=settings.google_api_key,
                temperature=temperature,
                streaming=streaming,
                **kwargs,
            )

        elif selected_provider == "openai":
            from langchain_openai import ChatOpenAI

            name = model_name or settings.openai_default_model
            return ChatOpenAI(
                model=name,
                api_key=settings.openai_api_key,
                temperature=temperature,
                streaming=streaming,
                **kwargs,
            )

        elif selected_provider == "groq":
            from langchain_groq import ChatGroq

            name = model_name or settings.groq_default_model
            return ChatGroq(
                model=name,
                api_key=settings.groq_api_key,
                temperature=temperature,
                streaming=streaming,
                **kwargs,
            )

        else:
            raise ValueError(
                f"Unsupported provider: '{selected_provider}'. "
                f"Choose from: 'google', 'openai', 'groq'."
            )


def get_chat_model(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    **kwargs,
) -> BaseChatModel:
    """Convenience helper to obtain a configured chat model."""
    return ModelFactory.create_model(
        provider=provider,
        model_name=model_name,
        temperature=temperature,
        **kwargs,
    )
