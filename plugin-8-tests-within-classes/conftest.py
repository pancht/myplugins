import pytest
import yaml


# Load test configuration and test data from YAML files
def load_yaml(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


# Load the YAML files
test_data = load_yaml("test_data.yml")['test_data']
test_config = load_yaml("test_config.yml")['test_config']


# Hook to modify test items and add user properties
def pytest_pycollect_makeitem(collector, name, obj):
    # If the collector is a class, modify the test items within the class
    if isinstance(collector, pytest.Class):
        # Loop through the test data and modify the test functions
        for data in test_data:
            # Add custom test properties based on test config
            test_name = data['name']
            param_1 = data['param_1']
            param_2 = data['param_2']

            # Create a new test function for each test data item
            item = collector.makeitem(f'{test_name}_{param_1}_{param_2}')

            # Assign custom user properties based on test configuration
            item.user_properties.append(('config_setting', test_config['setting_1']))
            item.user_properties.append(('test_param_1', param_1))
            item.user_properties.append(('test_param_2', param_2))

            # Add the item to the collector's items
            collector.items.append(item)

