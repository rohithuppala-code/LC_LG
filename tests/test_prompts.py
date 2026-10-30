"""Tests for prompt template compilation and variable bindings."""

from cogniflow.prompts.templates import get_research_prompt, get_fact_check_prompt


def test_research_prompt_formatting():
    prompt = get_research_prompt()
    formatted = prompt.format_messages(
        topic="Vector Databases",
        focus_areas="indexing algorithms, scalability",
        target_depth="deep technical",
    )
    assert len(formatted) == 2
    assert "Vector Databases" in formatted[1].content
    assert "indexing algorithms" in formatted[1].content


def test_fact_check_prompt_formatting():
    prompt = get_fact_check_prompt()
    formatted = prompt.format_messages(
        claim="Water boils at 100 degrees Celsius at sea level.",
        context="Standard atmospheric pressure",
    )
    assert len(formatted) == 2
    assert "Water boils at 100 degrees Celsius" in formatted[1].content
