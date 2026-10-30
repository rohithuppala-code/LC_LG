"""Tests for custom tools and mathematical evaluation."""

from cogniflow.tools.calculator import safe_eval_math, calculate_percentage_change


def test_safe_eval_math_basic():
    assert safe_eval_math.invoke({"expression": "10 + 25"}) == "35"
    assert safe_eval_math.invoke({"expression": "(4 * 5) + 12"}) == "32"
    assert safe_eval_math.invoke({"expression": "2 ** 4"}) == "16"


def test_safe_eval_math_invalid():
    res = safe_eval_math.invoke({"expression": "__import__('os').system('ls')"})
    assert "Calculation Error" in res


def test_calculate_percentage_change():
    res = calculate_percentage_change.invoke({"initial": 100.0, "current": 125.0})
    assert res == "+25.00%"

    res_drop = calculate_percentage_change.invoke({"initial": 200.0, "current": 150.0})
    assert res_drop == "-25.00%"


def test_percentage_change_zero_division():
    res = calculate_percentage_change.invoke({"initial": 0.0, "current": 50.0})
    assert "cannot be zero" in res
