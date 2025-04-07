# --- sentinel_plugin.py ---
import os
import yaml
import inspect
import pytest
from pathlib import Path
from _pytest.config import Config
from typing import Any


def load_all_test_data(data_dir: str) -> dict:
    test_definitions = {}
    for file in Path(data_dir).glob("*.yml"):
        with open(file, "r") as f:
            data = yaml.safe_load(f) or {}
            for key, val in data.items():
                if key in test_definitions:
                    test_definitions[key].extend(val)
                else:
                    test_definitions[key] = val
    return test_definitions


class SentinelPlugin:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.test_definitions = load_all_test_data(data_dir)

    def pytest_configure(self, config: Config):
        if hasattr(config, "workerinput"):
            config.test_definitions = config.workerinput.get("test_definitions")
        else:
            config.test_definitions = self.test_definitions

    def pytest_configure_node(self, node):
        node.workerinput["test_definitions"] = node.config.test_definitions

    def pytest_sessionstart(self, session):
        session.test_definitions = session.config.test_definitions

    def pytest_collection_modifyitems(self, session, config, items):
        for item in items:
            cls_name = item.parent.name if hasattr(item.parent, "name") else None
            method_name = item.name
            test_data = []
            if cls_name and cls_name in config.test_definitions:
                test_data.extend(config.test_definitions.get(cls_name, []))
            if method_name in config.test_definitions:
                test_data.extend(config.test_definitions.get(method_name, []))

            item.user_properties.append(("test_data", test_data))