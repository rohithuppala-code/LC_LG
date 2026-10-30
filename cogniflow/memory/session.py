"""Session-based chat history and conversational memory."""

from typing import Dict, Optional
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from cogniflow.models.factory import get_chat_model


class SessionManager:
    """Manages isolated chat message histories indexed by session ID."""

    def __init__(self):
        self._sessions: Dict[str, BaseChatMessageHistory] = {}

    def get_history(self, session_id: str) -> BaseChatMessageHistory:
        """Retrieve or create the message history for a given session."""
        if session_id not in self._sessions:
            self._sessions[session_id] = ChatMessageHistory()
        return self._sessions[session_id]

    def clear_session(self, session_id: str) -> bool:
        """Clear the history for a given session."""
        if session_id in self._sessions:
            self._sessions[session_id].clear()
            return True
        return False

    def list_sessions(self) -> list:
        """List all active session IDs."""
        return list(self._sessions.keys())


_GLOBAL_SESSION_MANAGER = SessionManager()


def get_session_manager() -> SessionManager:
    """Return the global session manager instance."""
    return _GLOBAL_SESSION_MANAGER


def create_conversational_chain(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    system_instruction: Optional[str] = None,
) -> RunnableWithMessageHistory:
    """Construct an LCEL chain with automated session message history tracking.

    Uses `MessagesPlaceholder(variable_name='chat_history')` to insert past dialogue.
    """
    model = get_chat_model(provider=provider, model_name=model_name, temperature=0.7)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_instruction
                or (
                    "You are a helpful, context-aware AI assistant. "
                    "Remember user details, past queries, and maintain coherent multi-turn dialogue."
                ),
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    base_chain = prompt | model | StrOutputParser()

    return RunnableWithMessageHistory(
        base_chain,
        get_session_history=_GLOBAL_SESSION_MANAGER.get_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
