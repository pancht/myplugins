import pytest


# Sample test class
class TestMathOperations:

    def test_addition(self, request):
        # Get user properties set by the hook
        config_setting = request.node.get_closest_marker("config_setting")
        test_param_1 = request.node.get_closest_marker("test_param_1")
        test_param_2 = request.node.get_closest_marker("test_param_2")

        # Perform a test operation using parameters
        result = test_param_1 + test_param_2
        assert result == (test_param_1 + test_param_2), f"Failed for config: {config_setting}."

    def test_multiplication(self, request):
        config_setting = request.node.get_closest_marker("config_setting")
        test_param_1 = request.node.get_closest_marker("test_param_1")
        test_param_2 = request.node.get_closest_marker("test_param_2")

        result = test_param_1 * test_param_2
        assert result == (test_param_1 * test_param_2), f"Failed for config: {config_setting}."
