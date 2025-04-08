def test_add(case):
    assert case["a"] + case["b"] == case["expected"]

class TestMathOperations:
    def test_subtract(self, case):
        assert case["a"] - case["b"] == case["expected"]
