# dynamic_pytest_framework/plugin.py
import pytest
import yaml
from pathlib import Path
from typing import Any
import inspect

def load_test_definitions(yaml_file):
    with open(yaml_file) as f:
        return yaml.safe_load(f)

class YamlTestItem(pytest.Function):
    def __init__(self, *args, test_metadata=None, **kwargs):
        self.test_metadata = test_metadata
        super().__init__(*args, **kwargs)

class YamlTestPlugin:
    def __init__(self, test_definitions):
        self.test_definitions = test_definitions

    def pytest_pycollect_makeitem(self, collector, name, obj):
        items = []
        if inspect.isclass(obj):
            # Match class name to YAML suite
            suite_def = self.test_definitions.get(name)
            if not suite_def:
                return []

            for test_def in suite_def["tests"]:
                method_name = test_def["name"]
                if hasattr(obj, method_name):
                    func = getattr(obj, method_name)
                    item = pytest.Function.from_parent(collector, name=method_name, callobj=func)
                    item.user_properties.append(("yaml_metadata", {
                        "suite_name": suite_def["suite_name"],
                        **test_def
                    }))
                    items.append(item)

        return items


# 🔥 Register command line option early
def pytest_addoption(parser):
    parser.addoption("--yaml", action="store", default="tests/test_suite.yml", help="Path to YAML test definition")

def pytest_configure(config):
    yaml_path = config.getoption("--yaml")
    test_definitions = load_test_definitions(yaml_path)
    plugin = YamlTestPlugin(test_definitions)
    config.pluginmanager.register(plugin, name="yaml_test_plugin")