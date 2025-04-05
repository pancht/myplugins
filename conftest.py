import pytest

pytest_plugins = ["dynamic_pytest_framework.plugin"]

@pytest.fixture(autouse=True)
def self(request):
    # fixture returning self for class-level fixtures
    # this is to handle, fixture "self" not found error
    # while debugging framework or individual test(s)
    yield request.cls


@pytest.fixture
def test_meta(request):
    for key, val in request.node.user_properties:
        if key == "yaml_metadata":
            return val
    return None


# @pytest.fixture
# def test_meta(request):
#     """Fixture to access test metadata from YAML."""
#     for key, value in request.node.user_properties:
#         if key == "yaml_metadata":
#             return value
#     return None
#
#
# # Class-Scoped Fixture with request Access
# # If you want to use test_meta for all tests in the class, you can:
# # Define a fixture that runs per-class
# @pytest.fixture(scope="class")
# def class_meta(request):
#     # request.node is the class, but we need to get one function item inside it
#     function_items = list(request.session.items)
#     for item in function_items:
#         if item.parent == request.node:
#             for key, value in item.user_properties:
#                 if key == "yaml_metadata":  # value from yml
#                     return value
#     return None