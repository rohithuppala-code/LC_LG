"""ReAct (Reasoning + Acting) Agent using modern LangChain tool binding."""

from typing import Any, Callable, Dict, List, Optional
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from cogniflow.models.factory import get_chat_model
from cogniflow.tools.registry import get_all_tools


class ReActAgent:
    """A tool-calling agent that iteratively reasons and invokes external tools."""

    def __init__(
        self,
        tools: Optional[List[BaseTool]] = None,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        max_iterations: int = 6,
        system_prompt: Optional[str] = None,
    ):
        self.tools = tools or get_all_tools()
        self.tool_map: Dict[str, BaseTool] = {t.name: t for t in self.tools}
        self.max_iterations = max_iterations

        base_model = get_chat_model(
            provider=provider,
            model_name=model_name,
            temperature=temperature,
        )
        # Bind the tools to the LLM
        self.model_with_tools = base_model.bind_tools(self.tools)

        self.system_prompt = system_prompt or (
            "You are CogniFlow's autonomous research assistant. "
            "You have access to tools for live web search, Wikipedia, and mathematical calculation. "
            "When answering questions requiring factual or computational precision, always invoke the appropriate tools. "
            "Synthesize your final response clearly with supporting evidence."
        )

    def run(
        self,
        query: str,
        on_thought: Optional[Callable[[str], None]] = None,
        on_tool_call: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        on_tool_result: Optional[Callable[[str, str], None]] = None,
    ) -> Dict[str, Any]:
        """Execute the agent loop until the final response is produced or max iterations reached.

        Returns:
            Dict containing 'answer', 'messages', 'iterations', and 'tool_history'.
        """
        messages: List[BaseMessage] = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=query),
        ]
        tool_history: List[Dict[str, Any]] = []

        for step in range(1, self.max_iterations + 1):
            if on_thought:
                on_thought(f"Step {step}: Reasoning about next action...")

            # Invoke the tool-bound model
            ai_message: AIMessage = self.model_with_tools.invoke(messages)
            messages.append(ai_message)

            # Check if the model requested any tool calls
            if not ai_message.tool_calls:
                return {
                    "answer": ai_message.content,
                    "messages": messages,
                    "iterations": step,
                    "tool_history": tool_history,
                }

            # Execute requested tool calls
            for tool_call in ai_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id", f"call_{step}")

                if on_tool_call:
                    on_tool_call(tool_name, tool_args)

                # Lookup and invoke tool safely
                if tool_name in self.tool_map:
                    try:
                        tool_output = self.tool_map[tool_name].invoke(tool_args)
                    except Exception as err:
                        tool_output = f"Tool execution failed: {str(err)}"
                else:
                    tool_output = f"Error: Tool '{tool_name}' not found."

                tool_str = str(tool_output)
                tool_history.append({
                    "step": step,
                    "tool": tool_name,
                    "args": tool_args,
                    "output": tool_str,
                })

                if on_tool_result:
                    on_tool_result(tool_name, tool_str)

                # Append tool observation back to messages for the LLM
                messages.append(
                    ToolMessage(
                        content=tool_str,
                        tool_call_id=tool_call_id,
                        name=tool_name,
                    )
                )

        return {
            "answer": "Reached maximum tool iterations without terminating.",
            "messages": messages,
            "iterations": self.max_iterations,
            "tool_history": tool_history,
        }


def create_react_agent(
    tools: Optional[List[BaseTool]] = None,
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
) -> ReActAgent:
    """Convenience factory to create a configured ReAct agent."""
    return ReActAgent(tools=tools, provider=provider, model_name=model_name)
