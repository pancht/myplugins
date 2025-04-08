# This works with case fixture (default)
import allure
import pytest


@allure.epic("Math Operations")
@allure.feature("Addition")
@allure.story("Simple add case")
@pytest.mark.functional
@pytest.mark.sanity
def test_add(case):
    assert case["a"] + case["b"] == case["expected"]


# This test uses multiple injected fixtures
@allure.epic("Math Operations")
@allure.feature("Multiply")
@allure.story("Simple multiply case")
@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.smoke
def test_multi_input(a, b, expected, integration, config):
    print(f"Running with {integration} and config {config}")
    assert a + b == expected


class TestMathOperations:
    @allure.epic("Math Operations")
    @allure.feature("Subtraction")
    @allure.story("Simple subtraction case")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.sanity
    def test_subtract(self, case, integration):
        assert case["a"] - case["b"] == case["expected"]
