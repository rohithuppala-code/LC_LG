"""Tests for session management and chat message history."""

from langchain_core.messages import HumanMessage, AIMessage
from cogniflow.memory.session import SessionManager


def test_session_manager_isolation():
    manager = SessionManager()

    hist_a = manager.get_history("session_alpha")
    hist_b = manager.get_history("session_beta")

    hist_a.add_message(HumanMessage(content="Hello from Alpha"))
    hist_b.add_message(HumanMessage(content="Hello from Beta"))

    assert len(hist_a.messages) == 1
    assert hist_a.messages[0].content == "Hello from Alpha"
    assert len(hist_b.messages) == 1
    assert hist_b.messages[0].content == "Hello from Beta"


def test_session_manager_clear():
    manager = SessionManager()
    hist = manager.get_history("session_temp")
    hist.add_message(AIMessage(content="Temporary response"))
    assert len(hist.messages) == 1

    cleared = manager.clear_session("session_temp")
    assert cleared is True
    assert len(manager.get_history("session_temp").messages) == 0
