import pytest

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

@pytest.mark.usefixtures("test_definitions")
class TestMathOperations:
    def test_add(self, test_definitions):
        for case in test_definitions["add"]:
            a, b, expected = case["a"], case["b"], case["expected"]
            assert add(a, b) == expected

    def test_subtract(self, test_definitions):
        for case in test_definitions["subtract"]:
            a, b, expected = case["a"], case["b"], case["expected"]
            assert subtract(a, b) == expected