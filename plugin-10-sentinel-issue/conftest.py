from my_class import MyClass

def pytest_generate_tests(metafunc):
    """
    Hook to dynamically parametrize fixtures used in tests.

    This function checks which fixtures are requested by a test class or function
    and injects parameter values accordingly. It supports indirect parametrization
    so the actual fixture functions can receive the parameter values via `request.param`.

    Fixtures supported:
    - fixture_obj: Injects instances of MyClass with different `my_param` values.
    - fixture_str: Injects plain strings (wrapped as MyClass instances in the fixture).

    Each parameter set is given a custom ID for clarity in test output.
    """

    # Parametrize 'fixture_obj' with two different MyClass instances
    if "fixture_obj" in metafunc.fixturenames:
        metafunc.parametrize(
            "fixture_obj",
            [MyClass("abc"), MyClass("cde")],
            indirect=True,
            ids=["obj1", "obj2"]
        )

    # Parametrize 'fixture_str' with two different strings
    if "fixture_str" in metafunc.fixturenames:
        metafunc.parametrize(
            "fixture_str",
            ["fgh", "ijk"],
            indirect=True,
            ids=["str1", "str2"]
        )
