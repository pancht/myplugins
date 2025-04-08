# This works with case fixture (default)
def test_add(case):
    assert case["a"] + case["b"] == case["expected"]


# This test uses multiple injected fixtures
def test_multi_input(a, b, expected, integration, config):
    print(f"Running with {integration} and config {config}")
    assert a + b == expected


class TestMathOperations:
    def test_subtract(self, case, integration):
        assert case["a"] - case["b"] == case["expected"]
