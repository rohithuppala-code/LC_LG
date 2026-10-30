"""Information retrieval tools wrapping DuckDuckGo and Wikipedia."""

from typing import List
from langchain_core.tools import tool


@tool
def search_duckduckgo(query: str, max_results: int = 4) -> str:
    """Search the live web using DuckDuckGo to obtain up-to-date information, news, and facts.

    Args:
        query: Search query terms.
        max_results: Maximum number of snippets to return (default 4).

    Returns:
        Consolidated markdown string containing titles, snippets, and source URLs.
    """
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                title = item.get("title", "")
                snippet = item.get("body", "")
                link = item.get("href", "")
                results.append(f"- **{title}**\n  {snippet}\n  *Source*: {link}")

        if not results:
            return f"No results found for query: '{query}'"

        return "\n\n".join(results)
    except Exception as exc:
        return f"Web Search Error: {str(exc)}"


@tool
def get_wikipedia_summary(entity: str, sentences: int = 3) -> str:
    """Retrieve an authoritative summary of a historical, scientific, or biographical subject from Wikipedia.

    Args:
        entity: The subject or topic name (e.g. 'Albert Einstein', 'LangChain', 'Transformer (deep learning architecture)').
        sentences: Number of summary sentences to retrieve (default 3).

    Returns:
        Summary text or disambiguation guidance.
    """
    try:
        import wikipedia

        wikipedia.set_lang("en")
        summary = wikipedia.summary(entity, sentences=sentences, auto_suggest=True)
        return summary
    except Exception as exc:
        return f"Wikipedia Retrieval Note: {str(exc)}"
