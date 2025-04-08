# This works with case fixture (default)
import allure
import pytest


@allure.epic("Math Operations")
@allure.feature("Addition")
@allure.story("Simple add case")
@pytest.mark.functional
@pytest.mark.sanity
@pytest.mark.testrail_id("C1000")
@pytest.mark.testrail_id("C1001")
def test_add(case):
    assert case["a"] + case["b"] == case["expected"]


# This test uses multiple injected fixtures
@allure.epic("Math Operations")
@allure.feature("Multiply")
@allure.story("Simple multiply case")
@pytest.mark.api
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.slow
@pytest.mark.testrail_id("C1002")
def test_multi_input(a, b, expected, integration, config):
    print(f"Running with {integration} and config {config}")
    assert a + b == expected


class TestMathOperations:
    @allure.epic("Math Operations")
    @allure.feature("Subtraction")
    @allure.story("Simple subtraction case")
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.sanity
    @pytest.mark.testrail_id("C1003")
    def test_subtract(self, case, integration):
        assert case["a"] - case["b"] == case["expected"]

def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        markers = item.iter_markers(name="testrail_id")
        for marker in markers:
            testrail_ids = marker.args[0]
            if isinstance(testrail_ids, str):
                testrail_ids = [testrail_ids]

            for case_id in testrail_ids:
                testrail_url = f"https://yourcompany.testrail.io/index.php?/cases/view/{case_id.lstrip('C')}"
                allure.dynamic.link(testrail_url, name=case_id)
