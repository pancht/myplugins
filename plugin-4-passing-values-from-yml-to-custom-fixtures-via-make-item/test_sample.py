import pytest

@pytest.mark.usefixtures("case_data")
class TestMathOperations:
    def test_add(self, case_data):
        assert case_data["a"] + case_data["b"] == case_data["expected"]

    def test_subtract(self, case_data):
        assert case_data["a"] - case_data["b"] == case_data["expected"]
