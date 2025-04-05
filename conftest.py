import pytest
import yaml
import os
from _pytest.config import Config
# No need to import when using x-dist
# from _pytest.nodes import WorkerInput


def pytest_addoption(parser):
    parser.addoption("--yaml", action="store", default="test_suite.yml", help="Path to YAML test suite")


def pytest_configure(config: Config):
    # Share test definitions to workers via config
    if hasattr(config, "workerinput"):
       return

    yaml_path = config.getoption("--yaml")
    with open(yaml_path, "r") as f:
        config.test_definitions = yaml.safe_load(f)


def pytest_configure_node(node):
    """Called in main process to configure a worker node."""
    node.workerinput["test_definitions"] = node.config.test_definitions

@pytest.fixture(scope="session")
def test_definitions(request):
    config = request.config
    if hasattr(config, "workerinput"):
        return config.workerinput["test_definitions"]
    return config.test_definitions