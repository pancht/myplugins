"""
Pytest hook for dynamic test parameterization using MyClass instances.

This configuration injects parameters into tests that require the 'fixture_obj'
fixture. It uses indirect parameterization to pass custom objects to the fixture,
enabling flexible and reusable test setups.
"""

from my_class import MyClass

def pytest_generate_tests(metafunc):
    """
    Hook to dynamically generate test parameters for the 'fixture_obj' fixture.

    If the fixture name 'fixture_obj' is detected in the test function,
    this hook applies indirect parameterization using an instance of MyClass.
    This allows the fixture to receive a fully constructed object rather than a raw value.

    Parameters:
        metafunc (Metafunc): Pytest-provided object that gives access to the test context
                             for parameterization and test generation.
    """
    if "fixture_obj" in metafunc.fixturenames:
        # Indirectly parametrize 'fixture_obj' using an instance of MyClass
        metafunc.parametrize(
            "fixture_obj",
            [MyClass("abc")],     # List of parameters passed to the fixture
            indirect=True,        # Tell pytest to pass the param to the fixture, not the test directly
            ids=["obj"]           # Custom ID for this parameter in test output
        )
