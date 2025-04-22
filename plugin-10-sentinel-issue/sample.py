"""
Pytest module demonstrating class-scoped, parameterized fixtures with UUID generation.

This test suite showcases how to use a class-scoped fixture that is parameterized
and cached per class instance to avoid repeated fixture execution. It also integrates
with pytest-xdist to group test execution within the same process for performance
and consistency.
"""

import logging
import uuid
from typing import Any
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def fixture_obj(request: Any):
    """
    Fixture that generates and returns a unique identifier per test class parameter.

    This fixture uses a combination of a parameter attribute and a UUID to build
    a unique string. The result is stored on the test class itself, ensuring it is
    reused across all test methods within the same parameterized test class instance.

    Parameters:
        request (Any): Pytest's built-in fixture providing access to the requesting test context.

    Returns:
        str: A unique, class-scoped string identifier.
    """
    if not hasattr(request.cls, "_fixture_obj"):
        my_param = request.param
        request.cls._fixture_obj = f"{my_param.my_param}--{str(uuid.uuid4())}"
    return request.cls._fixture_obj


class TestTestObj:
    """
    Example test class using a cached, parameterized class-scoped fixture.

    The fixture provides a unique identifier derived from a test parameter and
    a UUID, and is reused across all test methods. This class can be grouped
    in parallel test runs using `pytest-xdist` for scoped distribution.
    """

    def test_some_thing(self, fixture_obj):
        """
        Verifies the fixture value is accessible and outputs it.
        """
        print(fixture_obj)

    def test_some_think(self, fixture_obj):
        """
        Ensures the same fixture value is reused and prints it.
        """
        print(fixture_obj)
