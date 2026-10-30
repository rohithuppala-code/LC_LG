"""Tests for Pydantic schema validation."""

import pytest
from pydantic import ValidationError
from cogniflow.schemas.outputs import KeyInsight, ResearchReport, FactCheckResult


def test_key_insight_validation():
    insight = KeyInsight(
        category="Architecture",
        summary="LCEL decouples model binding from prompts.",
        impact_level="high",
        confidence_score=0.95,
    )
    assert insight.category == "Architecture"
    assert insight.confidence_score == 0.95


def test_key_insight_invalid_confidence():
    with pytest.raises(ValidationError):
        KeyInsight(
            category="Test",
            summary="Invalid score test",
            confidence_score=1.5,  # Out of range (max 1.0)
        )


def test_research_report_structure():
    report = ResearchReport(
        topic="LangGraph State Machines",
        executive_summary="LangGraph enables cyclic graphs for agent workflows.",
        pros=["State persistence", "Cyclic control loops"],
        cons=["Steeper learning curve"],
        action_items=["Adopt SQLite checkpointer"],
        verdict="Recommended for complex multi-agent architectures.",
    )
    assert report.topic == "LangGraph State Machines"
    assert len(report.pros) == 2
    assert len(report.cons) == 1


def test_fact_check_result():
    res = FactCheckResult(
        claim="Earth is the third planet from the sun.",
        verdict="verified_true",
        confidence=1.0,
        evidence="Astronomical consensus and planetary observations confirm this.",
    )
    assert res.verdict == "verified_true"
