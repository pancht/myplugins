import pytest

def add(a, b):
    return a + b

class MathTests:
    def test_add(self, test_data):
        for case in test_data:
            assert add(case["a"], case["b"]) == case["expected"]