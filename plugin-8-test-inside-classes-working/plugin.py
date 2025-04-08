import pytest
import yaml
import os
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption("--data-dir", action="store", default="test_data", help="Directory containing YAML files")


def load_yaml_data(yaml_dir):
    test_data = {}
    for file in Path(yaml_dir).glob("*.yml"):
        with open(file, "r") as f:
            class_name = file.stem
            test_data[class_name] = yaml.safe_load(f)
    return test_data


def pytest_configure(config):
    data_dir = config.getoption("--data-dir")
    config.test_data = load_yaml_data(data_dir)


@pytest.fixture(scope="session")
def test_data(request):
    return request.config.test_data


def pytest_generate_tests(metafunc):
    cls = metafunc.cls
    if cls is None:
        return

    class_name = cls.__name__
    data = metafunc.config.test_data.get(class_name, {})

    if metafunc.function.__name__ in data:
        values = data[metafunc.function.__name__]
        metafunc.parametrize("case", values)
