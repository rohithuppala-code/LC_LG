"""Prompt templates using LangChain ChatPromptTemplate primitives."""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

RESEARCH_SYSTEM_INSTRUCTION = """You are an elite, objective senior research analyst.
Your goal is to conduct comprehensive, nuanced inquiries into topics provided by the user.

Adhere strictly to the following principles:
1. Objectivity: Present balanced evidence without subjective bias.
2. Structure: Break down complex concepts into categorized, atomic insights.
3. Critical Analysis: Explicitly weigh advantages against trade-offs and potential failure modes.
4. Actionability: Every recommendation must be concrete, specific, and pragmatic.
"""

FACT_CHECK_SYSTEM_INSTRUCTION = """You are a rigorous, evidence-driven factual auditor.
Your job is to critically evaluate claims against established scientific, empirical, and industry standards.

Rules:
- State a clear verdict: verified_true, partially_true, false, or unverifiable.
- Provide direct citations or logical reasoning supporting your assessment.
- Highlight counter-arguments or edge cases where the claim might differ.
"""

RESEARCH_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(RESEARCH_SYSTEM_INSTRUCTION),
        HumanMessagePromptTemplate.from_template(
            "Topic for Investigation: {topic}\n\n"
            "Key Focus Areas: {focus_areas}\n"
            "Target Audience / Depth: {target_depth}\n\n"
            "Produce an authoritative, deeply structured analysis."
        ),
    ]
)

FACT_CHECK_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(FACT_CHECK_SYSTEM_INSTRUCTION),
        HumanMessagePromptTemplate.from_template(
            "Claim to verify: {claim}\n"
            "Context (if any): {context}\n\n"
            "Perform rigorous fact-checking and return a structured verdict."
        ),
    ]
)

COMPARISON_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(RESEARCH_SYSTEM_INSTRUCTION),
        HumanMessagePromptTemplate.from_template(
            "Perform a rigorous side-by-side comparative analysis:\n"
            "- Option A: {option_a}\n"
            "- Option B: {option_b}\n"
            "- Evaluation Criteria: {criteria}\n\n"
            "Highlight strengths, weaknesses, best-fit use cases, and give a decisive recommendation."
        ),
    ]
)


def get_research_prompt() -> ChatPromptTemplate:
    """Return the pre-configured research prompt template."""
    return RESEARCH_PROMPT_TEMPLATE


def get_fact_check_prompt() -> ChatPromptTemplate:
    """Return the pre-configured fact-checking prompt template."""
    return FACT_CHECK_PROMPT_TEMPLATE
