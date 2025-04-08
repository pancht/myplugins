import pytest
import yaml
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption(
        "--data-dir", action="store", default="test_data", help="Path to YAML test data directory"
    )


def load_test_data(data_dir):
    all_data = {}
    data_path = Path(data_dir)
    for yml_file in data_path.glob("*.yml"):
        with yml_file.open() as f:
            data = yaml.safe_load(f) or {}
            all_data[yml_file.stem] = data
    return all_data


def pytest_configure(config):
    config.test_data = load_test_data(config.getoption("--data-dir"))


def pytest_generate_tests(metafunc):
    module_name = Path(metafunc.definition.fspath).stem
    test_data = metafunc.config.test_data.get(module_name, {})

    # Determine if test is in a class
    if metafunc.cls:
        class_data = test_data.get(metafunc.cls.__name__, {})
        params = class_data.get(metafunc.function.__name__, [])
    else:
        params = test_data.get(metafunc.function.__name__, [])

    # Support multiple fixtures if test wants them
    # We assume the YAML entry is a dict with keys mapping to fixture names
    if params:
        if isinstance(params[0], dict):
            keys = list(params[0].keys())
            if set(keys) & set(metafunc.fixturenames):
                used_keys = [k for k in keys if k in metafunc.fixturenames]
                metafunc.parametrize(used_keys, [[p[k] for k in used_keys] for p in params])
            else:
                metafunc.parametrize("case", params)
        else:
            metafunc.parametrize("case", params)


# Example additional fixture
@pytest.fixture
def integration():
    return "integration-db-session"


@pytest.fixture
def config():
    return {"env": "staging", "timeout": 30}
