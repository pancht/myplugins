import pytest
from sentinel_plugin import SentinelPlugin

def pytest_addoption(parser):
    parser.addoption("--data-dir", action="store", default="test_data", help="Directory with YAML test inputs")

def pytest_configure(config):
    data_dir = config.getoption("--data-dir")
    plugin = SentinelPlugin(data_dir)
    config.pluginmanager.register(plugin, name="sentinel-plugin")

@pytest.fixture(scope="function")
def test_data(request):
    for name, value in request.node.user_properties:
        if name == "test_data":
            return value
    return []