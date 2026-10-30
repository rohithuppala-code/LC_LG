"""Parallel LCEL composition using RunnableParallel, RunnablePassthrough, and RunnableLambda."""

from typing import Any, Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from cogniflow.models.factory import get_chat_model


def format_parallel_output(results: Dict[str, Any]) -> Dict[str, Any]:
    """Combine and post-process outputs from parallel branches."""
    return {
        "subject": results["topic"],
        "executive_summary": results["summary"].strip(),
        "pros_and_cons": results["analysis"].strip(),
        "metadata": {
            "branches_evaluated": ["summary", "analysis"],
            "status": "success",
        },
    }


def create_parallel_analysis_chain(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
) -> Runnable:
    """Build an LCEL pipeline executing multiple reasoning paths simultaneously.

    Architecture:
                        /-> summary_chain  -\
        input (topic) ->                     -> format_parallel_output
                        \-> analysis_chain -/
    """
    model = get_chat_model(provider=provider, model_name=model_name, temperature=0.4)
    parser = StrOutputParser()

    # Branch 1: High-level executive synthesis
    summary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an executive briefer. Write a 3-sentence summary of the subject."),
            ("human", "Subject: {topic}"),
        ]
    )
    summary_branch = summary_prompt | model | parser

    # Branch 2: Deep pros and cons breakdown
    analysis_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a critical strategist. List 3 key advantages and 3 trade-offs/risks."),
            ("human", "Subject: {topic}"),
        ]
    )
    analysis_branch = analysis_prompt | model | parser

    # Parallel orchestrator combining both branches
    parallel_map = RunnableParallel(
        topic=RunnablePassthrough(),
        summary=summary_branch,
        analysis=analysis_branch,
    )

    return parallel_map | RunnableLambda(format_parallel_output)
