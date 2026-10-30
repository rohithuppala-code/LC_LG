"""LCEL chains producing structured, Pydantic-validated responses."""

from typing import Optional
from langchain_core.runnables import Runnable
from cogniflow.models.factory import get_chat_model
from cogniflow.prompts.templates import get_research_prompt, get_fact_check_prompt
from cogniflow.schemas.outputs import ResearchReport, FactCheckResult


def create_research_chain(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.3,
) -> Runnable:
    """Build an LCEL chain that analyzes a topic and returns a structured ResearchReport.

    Pipeline:
        input_dict -> ChatPromptTemplate -> LLM (with_structured_output) -> ResearchReport
    """
    model = get_chat_model(
        provider=provider,
        model_name=model_name,
        temperature=temperature,
    )
    prompt = get_research_prompt()
    structured_llm = model.with_structured_output(ResearchReport)

    # LCEL pipeline using the pipe operator |
    return prompt | structured_llm


def create_fact_check_chain(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.0,
) -> Runnable:
    """Build an LCEL chain that fact-checks a claim and returns FactCheckResult.

    Pipeline:
        input_dict -> ChatPromptTemplate -> LLM (with_structured_output) -> FactCheckResult
    """
    model = get_chat_model(
        provider=provider,
        model_name=model_name,
        temperature=temperature,
    )
    prompt = get_fact_check_prompt()
    structured_llm = model.with_structured_output(FactCheckResult)

    return prompt | structured_llm
