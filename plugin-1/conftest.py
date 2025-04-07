import pytest
import yaml
from _pytest.config import Config

class SentinelPlugin:
    def __init__(self):
        self.test_definitions = {}

    def pytest_configure(self, config: Config):
        yaml_path = config.getoption("--yaml")
        with open(yaml_path, "r") as f:
            self.test_definitions = yaml.safe_load(f)
        config.test_definitions = self.test_definitions

    def pytest_configure_node(self, node):
        node.workerinput["test_definitions"] = node.config.test_definitions

@pytest.fixture(scope="session")
def test_definitions(request):
    config = request.config
    if hasattr(config, "workerinput"):
        return config.workerinput["test_definitions"]
    return config.test_definitions


# ✅ Register the CLI option once
def pytest_addoption(parser):
    parser.addoption(
        "--yaml",
        action="store",
        default="test_data.yml",
        help="Path to YAML test suite",
    )

# ✅ Register plugin instance once
def pytest_configure(config):
    plugin = SentinelPlugin()
    config.pluginmanager.register(plugin, name="sentinel-plugin")
