"""LCEL Chains and workflow composition."""

from cogniflow.chains.structured_chain import (
    create_research_chain,
    create_fact_check_chain,
)
from cogniflow.chains.parallel_chain import create_parallel_analysis_chain

__all__ = [
    "create_research_chain",
    "create_fact_check_chain",
    "create_parallel_analysis_chain",
]
