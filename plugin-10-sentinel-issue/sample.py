import logging
import uuid
from typing import Any
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def fixture_obj(request: Any):
    """
    Class-scoped fixture that generates and caches a unique string per parameterized MyClass instance.

    The returned string is composed of the `my_param` attribute and a UUID.
    Cached values are stored per test class and per parameter value to ensure uniqueness
    across parameter sets within the same test class.

    Example return: "abc--550e8400-e29b-41d4-a716-446655440000"
    """
    param_key = request.param.my_param  # Use the value of `my_param` as cache key
    if not hasattr(request.cls, "_fixture_obj_cache"):
        request.cls._fixture_obj_cache = {}  # Initialize cache dictionary
    if param_key not in request.cls._fixture_obj_cache:
        # Generate and store a unique string for this parameter
        request.cls._fixture_obj_cache[param_key] = f"{param_key}--{str(uuid.uuid4())}"
    return request.cls._fixture_obj_cache[param_key]


@pytest.fixture(scope="class")
def fixture_str(request: Any):
    """
    Class-scoped fixture that generates and caches a unique string per plain string parameter.

    The returned string is the original string parameter combined with a UUID.
    Cached values are stored per test class and per parameter value to ensure uniqueness
    across parameter sets within the same test class.

    Example return: "fgh--550e8400-e29b-41d4-a716-446655440000"
    """
    param_key = request.param  # Use the raw string parameter as cache key
    if not hasattr(request.cls, "_fixture_str_cache"):
        request.cls._fixture_str_cache = {}  # Initialize cache dictionary
    if param_key not in request.cls._fixture_str_cache:
        # Generate and store a unique string for this parameter
        request.cls._fixture_str_cache[param_key] = f"{param_key}--{str(uuid.uuid4())}"
    return request.cls._fixture_str_cache[param_key]


class TestTestObj:
    """
    Test class for scenarios using 'fixture_obj', which is based on MyClass instances.
    """

    def test_some_thing(self, fixture_obj):
        print(fixture_obj)

    def test_some_think(self, fixture_obj):
        print(fixture_obj)


class TestTestStr:
    """
    Test class for scenarios using 'fixture_str', which is based on plain string parameters.
    """

    def test_some_thing(self, fixture_str):
        print(fixture_str)

    def test_some_think(self, fixture_str):
        print(fixture_str)
