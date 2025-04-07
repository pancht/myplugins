import pytest
import yaml
from pathlib import Path
import inspect
from _pytest.python import Module

def pytest_addoption(parser):
    parser.addoption("--data-dir", action="store", default="test_data", help="Directory with YAML test data")

def pytest_configure(config):
    data_dir = Path(config.getoption("--data-dir"))
    test_data = {}
    for yml in data_dir.glob("*.yml"):
        with open(yml) as f:
            test_data[yml.stem] = yaml.safe_load(f)
    config._yaml_test_data = test_data


def pytest_pycollect_makeitem(collector, name, obj):
    config = collector.config
    #
    # if inspect.isclass(obj) and name.startswith("Test"):
    #     return [CustomItem.from_parent(collector, name=name, obj=obj)]

    if inspect.isfunction(obj) and name.startswith("test_"):
        if isinstance(collector, Module):
            class_name = collector.name
            class_name = class_name.replace("test_", "").replace(".py", "")
        else:
            class_name = collector.parent.name if hasattr(collector.parent, 'name') else None

        if class_name and class_name in config._yaml_test_data:
            data = config._yaml_test_data[class_name].get(name)
            if data:
                items = []
                for idx, params in enumerate(data):
                    item = pytest.Function.from_parent(collector, name=f"{name}[{idx}]", callobj=obj)
                    item.funcargs = {'input_data': params}
                    items.append(item)
                return items
    return None

@pytest.fixture
def abc(request):
    return request

@pytest.fixture
def input_data(abc):
    return abc._pyfuncitem.funcargs['input_data']

