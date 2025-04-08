import logging
import re
import sys
from colorsys import yiq_to_rgb

import allure
import pytest
import yaml
from pathlib import Path
import inspect
from _pytest.python import Module
import shutil
import os
import pytest

def marker_support(config):
    markers = [
        "ui: marks UI tests",
        "regression: marks regression suite",
        "api: marks API-related tests",
        "sanity: marks sanity check tests",
        "smoke: marks smoke suite",
        "integration: marks integration tests",
        "functional: marks functional tests",
        "resilience: marks resilience testing",
        "component: marks component-level tests",
        "fault_tolerance: marks fault tolerance tests",
        "slow: marks slow tests",
        "testrail_id(id): Link test case to TestRail ID"
    ]

    for marker in markers:
        config.addinivalue_line("markers", marker)

def delete_file_if_exists(file_name: str):
    file_path = Path(file_name)

    # Check if the file exists and delete it
    if file_path.exists():
        file_path.unlink()
        print(f"file {file_name} deleted.")
    else:
        print(f"file {file_name} does not exist.")

def is_worker(config):
    return hasattr(config, "workerinput")

def process_name(config) -> str:
    return "worker" if is_worker(config) else "master"

def pytest_sessionstart(session):
    # Log once when session starts to confirm collection is complete
    logging.info(f"Session started by {process_name(session.config)} process")
    # move current allure results to history
    # move_allure_results_to_history()


def pytest_addoption(parser):
    parser.addoption(
        "--data-dir", action="store", default="test_data", help="Path to YAML test data directory"
    )


def load_test_data(data_dir):
    all_data = {}
    data_path = Path(data_dir)
    for yml_file in data_path.glob("*.yml"):
        with yml_file.open() as f:
            data = yaml.safe_load(f) or {}
            all_data[yml_file.stem] = data
    return all_data


def pytest_configure(config):
    log_file = 'test_execution.log'
    delete_file_if_exists(log_file)
    # Set up logging configuration
    logging.basicConfig(
        filename=log_file,  # Log file name
        level=logging.DEBUG,  # Log level (DEBUG to capture everything)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    )
    logging.info(f"pytest_configure is called - once per session by {process_name(config)} process")

    config.test_data = load_test_data(config.getoption("--data-dir"))

    # add markers
    marker_support(config)

def pytest_generate_tests(metafunc):
    logging.info(f"pytest_generate_tests called by {process_name(metafunc.config)} process")
    module_name = Path(metafunc.definition.fspath).stem
    test_data = metafunc.config.test_data.get(module_name, {})

    # Determine if test is in a class
    if metafunc.cls:
        class_data = test_data.get(metafunc.cls.__name__, {})
        params = class_data.get(metafunc.function.__name__, [])
    else:
        params = test_data.get(metafunc.function.__name__, [])

    # Support multiple fixtures if test wants them
    # We assume the YAML entry is a dict with keys mapping to fixture names
    if params:
        if isinstance(params[0], dict):
            keys = list(params[0].keys())
            if set(keys) & set(metafunc.fixturenames):
                used_keys = [k for k in keys if k in metafunc.fixturenames]
                metafunc.parametrize(used_keys, [[p[k] for k in used_keys] for p in params])
            else:
                metafunc.parametrize("case", params)
        else:
            metafunc.parametrize("case", params)


# Example additional fixture
@pytest.fixture
def integration(request):
    logging.info(f"From integration fixture by {process_name(request.config)} process")
    yield "integration-db-session"
    logging.info("Destroy integration")


@pytest.fixture
def config(request):
    logging.info(f"from config fixture by {process_name(request.config)} process")
    yield {"env": "staging", "timeout": 30}
    logging.info("Destroy config")

#
# def pytest_runtest_teardown(item, nextitem):
#     with allure.step(f"Global Teardown for: {item.name}"):
#         allure.attach(f"Cleaning up after test: {item.name}", name="global-teardown", attachment_type=allure.attachment_type.TEXT)