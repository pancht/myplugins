import pytest
import yaml
import os
from _pytest.config import Config
# No need to import when using x-dist
# from _pytest.nodes import WorkerInput


def pytest_addoption(parser):
    parser.addoption("--yaml", action="store", default="test_suite.yml", help="Path to YAML test suite")


def pytest_configure(config: Config):
    # Read yaml definitions and share test definitions
    # to workers via config in order to be compatible with pytest-xdist.
    worker_process: bool = hasattr(config, "workerinput")
    if not worker_process:  # master process in pytest-xdist
        yaml_path = config.getoption("--yaml")  # read yaml
        with open(yaml_path, "r") as f:
            config.test_definitions = yaml.safe_load(f)

@pytest.fixture(scope="session")
def test_definitions(request):
    config = request.config
    worker_process: bool = hasattr(config, "workerinput")
    if worker_process:
        return config.workerinput["test_definitions"]
    return config.test_definitions

def pytest_configure_node(node):
    """This hook is called by the main process to configure a worker node by pytest-xdist plugin."""
    node.workerinput["test_definitions"] = node.config.test_definitions

