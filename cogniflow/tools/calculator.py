"""Safe mathematical tools for calculation and quantitative reasoning."""

import ast
import operator
from langchain_core.tools import tool

# Supported safe operators
_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _SAFE_OPERATORS:
            return _SAFE_OPERATORS[op_type](_safe_eval(node.left), _safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in _SAFE_OPERATORS:
            return _SAFE_OPERATORS[op_type](_safe_eval(node.operand))
    raise ValueError(f"Unsupported mathematical expression or operator: {node}")


@tool
def safe_eval_math(expression: str) -> str:
    """Safely evaluates a basic mathematical expression without using dangerous eval.

    Supports addition (+), subtraction (-), multiplication (*), division (/), modulo (%), and exponents (**).

    Args:
        expression: Mathematical expression string, e.g. '(15 * 4) + 12.5'

    Returns:
        The calculated result as a string, or an error message.
    """
    try:
        parsed = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(parsed.body)
        return str(result)
    except Exception as exc:
        return f"Calculation Error: {str(exc)}"


@tool
def calculate_percentage_change(initial: float, current: float) -> str:
    """Calculate the percentage increase or decrease from an initial value to a current value.

    Args:
        initial: The baseline value.
        current: The new/current value.

    Returns:
        Formatted percentage change, e.g. '+25.40%' or '-10.15%'.
    """
    if initial == 0:
        return "Error: Initial value cannot be zero."
    change = ((current - initial) / initial) * 100
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:.2f}%"
