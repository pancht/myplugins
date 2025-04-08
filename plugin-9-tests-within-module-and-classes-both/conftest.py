import logging

import pytest
import yaml
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption(
        "--data-dir", action="store", default="test_data", help="Directory with YAML test data"
    )


def load_yaml_data(data_dir):
    all_data = {}
    for yml_file in Path(data_dir).glob("*.yml"):
        module_name = yml_file.stem
        with open(yml_file) as f:
            data = yaml.safe_load(f) or {}
            all_data[module_name] = data
    return all_data


def pytest_configure(config):
    config.test_data = load_yaml_data(config.getoption("--data-dir"))


def pytest_generate_tests(metafunc):
    module_name = Path(metafunc.definition.fspath).stem
    data = metafunc.config.test_data.get(module_name, {})

    # class-based test
    if metafunc.cls:
        class_name = metafunc.cls.__name__
        class_data = data.get(class_name, {})
        cases = class_data.get(metafunc.function.__name__, [])
    else:
        # module-level function test
        cases = data.get(metafunc.function.__name__, [])

    if cases:
        metafunc.parametrize("case", cases)


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
    request.node.user_properties.append(("source", source))
    yield source

@pytest.fixture
def destination(request):
    logging.info("From destination fixture")
    destination = Destination(request.node.user_properties)
    request.node.user_properties.append(("destination", destination))
    yield destination

@pytest.fixture
def integration(source, destination):
    logging.info("From integration fixture")
    integration = Integration(source, destination)
    yield integration
    logging.info("Destroy integration")