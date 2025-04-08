class TestMathOperations:
    def test_add(self, case):
        assert case["a"] + case["b"] == case["expected"]

    def test_subtract(self, case):
        assert case["a"] - case["b"] == case["expected"]
