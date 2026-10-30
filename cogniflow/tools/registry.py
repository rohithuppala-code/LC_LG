"""Central registry and grouping for CogniFlow tools."""

from typing import List
from langchain_core.tools import BaseTool
from cogniflow.tools.calculator import safe_eval_math, calculate_percentage_change
from cogniflow.tools.web_search import search_duckduckgo, get_wikipedia_summary


def get_research_tools() -> List[BaseTool]:
    """Return tools tailored for informational research and fact checking."""
    return [
        search_duckduckgo,
        get_wikipedia_summary,
    ]


def get_all_tools() -> List[BaseTool]:
    """Return all available tools in the registry."""
    return [
        search_duckduckgo,
        get_wikipedia_summary,
        safe_eval_math,
        calculate_percentage_change,
    ]
