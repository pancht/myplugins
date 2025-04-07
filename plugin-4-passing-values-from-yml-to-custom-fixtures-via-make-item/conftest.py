import pytest
from sentinel_plugin import SentinelPlugin


def pytest_addoption(parser):
    parser.addoption("--data-dir", action="store", default="test_data", help="Path to YAML test suite directory")

def pytest_configure(config):
    plugin = SentinelPlugin()
    plugin.pytest_addoption(config._parser)
    plugin.pytest_configure(config)
    config.pluginmanager.register(plugin, name="sentinel_plugin")

@pytest.fixture
def case_data(request):
    for key, value in request.node.user_properties:
        if key == "case_data":
            return value
    return {}

