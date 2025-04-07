# --- sentinel_plugin.py ---
import os
import yaml
import inspect
import pytest
from pathlib import Path
from _pytest.config import Config
from _pytest.nodes import Collector, Item
from typing import Any

class SentinelPlugin:
    def __init__(self):
        self.test_data = {}

    def pytest_addoption(self, parser):
        try:
            parser.addoption("--data-dir", action="store", default="test_data", help="Path to YAML test suite directory")
        except ValueError:
            pass

    def pytest_configure(self, config: Config):
        data_dir = config.getoption("--data-dir")
        self.test_data = self._load_test_data(data_dir)
        config.test_data = self.test_data
        if hasattr(config, "workerinput"):
            config.workerinput["test_data"] = self.test_data

    def pytest_sessionstart(self, session):
        config = session.config
        if hasattr(config, "workerinput"):
            config.test_data = config.workerinput.get("test_data", {})

    def pytest_pycollect_makeitem(self, collector: Collector, name: str, obj: Any):
        if inspect.isfunction(obj) and name.startswith("test_"):
            parent_cls_name = getattr(collector.obj, "__name__", None)
            class_data = collector.config.test_data.get(parent_cls_name, {})
            test_data = class_data.get(name, [])

            items = []
            for i, case in enumerate(test_data):
                nodeid = f"{name}[case{i}]"
                item = pytest.Function.from_parent(collector, name=nodeid, callobj=obj)
                item.user_properties.append(("case_data", case))
                items.append(item)

            return items
        return None

    def _load_test_data(self, data_dir):
        test_data = {}
        for fname in os.listdir(data_dir):
            if fname.endswith(".yml") or fname.endswith(".yaml"):
                class_name = fname.replace(".yml", "").replace(".yaml", "")
                with open(os.path.join(data_dir, fname)) as f:
                    test_data[class_name] = yaml.safe_load(f)
        return test_data

#
# def pytest_configure(config):
#     plugin = SentinelPlugin()
#     plugin.pytest_addoption(config._parser)
#     plugin.pytest_configure(config)
#     config.pluginmanager.register(plugin, name="sentinel_plugin")