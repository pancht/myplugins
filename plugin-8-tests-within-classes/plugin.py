import logging
import yaml
import os
from pathlib import Path
import pytest
from _pytest.python import Module, Class
import inspect


def load_test_data(config):
    # Load test data from YAML files
    data_dir = Path(config.getoption("--data-dir", "test_data"))
    test_data = {}
    for yml in data_dir.glob("*.yml"):
        with open(yml) as f:
            test_data[yml.stem] = yaml.safe_load(f)
    return test_data


def pytest_addoption(parser):
    # Add an option to specify the directory for test data
    parser.addoption("--data-dir", action="store", default="test_data", help="Directory containing YAML test data")


def pytest_configure(config):
    # Load test data when pytest configures
    test_data = load_test_data(config)
    config._yaml_test_data = test_data
    logging.info("Test data loaded from YAML files")


def pytest_pycollect_makeitem(collector, name, obj):
    config = collector.config
    _yaml_test_data = config._yaml_test_data

    if inspect.isfunction(obj) or inspect.ismethod(obj):
        # If the item is a function or method (could be within a class)
        module_name = collector.parent.name if isinstance(collector, Class) else collector.name
        module_name = module_name.replace("test_", "").replace(".py", "")

        # Check if we have test data for this module and function/method
        if module_name and module_name in _yaml_test_data:
            test_data = _yaml_test_data[module_name].get(name)
            if test_data:
                items = []
                for idx, params in enumerate(test_data):
                    # Create a parameterized test item with the parameters
                    item = pytest.Function.from_parent(collector, name=f"{name}[{idx}]", callobj=obj)
                    item.funcargs = {"input_data": params}
                    items.append(item)
                return items
    return None


class Source:
    def __init__(self, user_properties: dict):
        self.user_properties = user_properties


class Destination:
    def __init__(self, user_properties: dict):
        self.user_properties = user_properties


class Integration:
    def __init__(self, source: Source, destination: Destination):
        self.source = source
        self.destination = destination


@pytest.fixture
def source(request):
    # Set up the source fixture
    source = Source(request.node.user_properties)
    request.node.user_properties.append(("source", source))
    yield source


@pytest.fixture
def destination(request):
    # Set up the destination fixture
    destination = Destination(request.node.user_properties)
    request.node.user_properties.append(("destination", destination))
    yield destination


@pytest.fixture
def integration(source, destination):
    # Set up the integration fixture
    integration = Integration(source, destination)
    yield integration


@pytest.fixture
def input_data(request):
    # Provide the test data from the parameterized tests
    return request.node.user_properties["input_data"]
