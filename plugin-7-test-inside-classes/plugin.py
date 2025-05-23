import logging
import re
import sys

import pytest
import yaml
from pathlib import Path
import inspect
from _pytest.python import Module
import shutil
import os
import pytest


# Path to your allure results and history directories
ALLURE_RESULTS_DIR = "allure-results"
ALLURE_HISTORY_DIR = "allure-history"

def move_allure_results_to_history():
    # Check if the allure-results directory exists
    if os.path.exists(ALLURE_RESULTS_DIR):
        # If allure-results exists, move it to allure-history
        if not os.path.exists(ALLURE_HISTORY_DIR):
            os.makedirs(ALLURE_HISTORY_DIR)  # Create allure-history if it doesn't exist
        shutil.move(ALLURE_RESULTS_DIR, ALLURE_HISTORY_DIR)
        # print(f"Moved {ALLURE_RESULTS_DIR} to {ALLURE_HISTORY_DIR}")
    else:
        # print(f"No {ALLURE_RESULTS_DIR} directory found.")
        pass

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
    logging.info("Session started - tests are collected")
    # move current allure results to history
    # move_allure_results_to_history()

def pytest_addoption(parser):
    parser.addoption("--data-dir", action="store", default="test_data", help="Directory with YAML test data")

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

    data_dir = Path(config.getoption("--data-dir"))
    test_data = {}
    for yml in data_dir.glob("*.yml"):
        with open(yml) as f:
            test_data[yml.stem] = yaml.safe_load(f)
    config._yaml_test_data = test_data

    logging.info(f"cache: {config.cache}")
    # Use config.cache to share data with workers
    config.cache.set('_yaml_test_data', test_data)



def pytest_pycollect_makeitem(collector, name, obj):
    config = collector.config
    logging.info(f"Collecting test item: {name}")
    _yaml_test_data = config.cache.get('_yaml_test_data', None)

    if inspect.isfunction(obj) and name.startswith("test_"):
        if isinstance(collector, Module):
            module_name = collector.name
            module_name = re.sub(r"^test_|\.py$", "", module_name)
        else:
            module_name = collector.parent.name if hasattr(collector.parent, 'name') else None

        if module_name and module_name in _yaml_test_data:
            data = _yaml_test_data[module_name].get(name)
            if data:
                items = []
                for idx, params in enumerate(data):
                    item = pytest.Function.from_parent(collector, name=f"{name}[{idx}]", callobj=obj)
                    item.funcargs = {'input_data': params}
                    item.user_properties = {'input_data': params}
                    items.append(item)
                return items
    return None

class Source:
    def __init__(self, user_properties: dict):
        self.msg = "initialize source"
        self.user_properties = user_properties

class Destination:
    def __init__(self, user_properties: dict):
        self.msg = "initialize destination"
        self.user_properties = user_properties

class Integration(Source, Destination):
    def __init__(self, source: Source, destination: Destination):
        self.source = source
        self.destination = destination
        self.msg = "initialize integration"

@pytest.fixture
def source(request):
    logging.info("From source fixture")
    source = Source(request.node.user_properties)
    request.node.user_properties["source"] = source
    yield source

@pytest.fixture
def destination(request):
    logging.info("From destination fixture")
    destination = Destination(request.node.user_properties)
    yield destination

@pytest.fixture
def integration(source, destination):
    logging.info("From integration fixture")
    integration = Integration(source, destination)
    yield integration
    logging.info("Destroy integration")

@pytest.fixture
def input_data():
    logging.info("from input_data fixture")
    return source._pyfuncitem.funcargs['input_data']


# --------------------
# Example plugin that passes test-configs via request
# Sequence of calls
# input_data -> abc
# abc fixture consumes test-configs via request read from yaml
# passes back test-config to input_data fixture
# its upto test if it wants to consume test-config.
#
# Following are Limitations and Features as of now.
#
# Limitations:
# 1. It does not support test withing test classes.
#
# Feature:
# Parameterizes tests from input values to each test from the yaml.

