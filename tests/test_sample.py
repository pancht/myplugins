import pytest


@pytest.mark.usefixtures
class TestMathOps:
    def test_add(self, test_meta):
        p = test_meta["params"]
        assert p["a"] + p["b"] == p["expected"]

    def test_subtract(self, test_meta):
        p = test_meta["params"]
        assert p["a"] - p["b"] == p["expected"]


# def test_example(test_meta):
#     assert "id" in test_meta
#     print(f"Running test ID: {test_meta['id']}")


# def test_addition(test_meta):
#     a = test_meta["params"]["a"]
#     b = test_meta["params"]["b"]
#     expected = test_meta["params"]["expected"]
#     assert a + b == expected

# Case: Tests Inside a Class
# This works exactly the same because request.node still points to the current test item, even inside a class.
# class TestMathOps:
#     # use class scoped fixture class_meta in the class as test parameter.
#     def test_add(self, class_meta):
#         print(f"[Class Scoped] Test ID: {class_meta['id']}")

