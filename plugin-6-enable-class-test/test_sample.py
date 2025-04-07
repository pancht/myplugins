import logging

import pytest

from plugin import Integration

def test_add(input_data, integration: Integration):
    logging.info("from test test_add")
    assert integration.source.user_properties["input_data"] == input_data
    assert integration.destination.user_properties["input_data"] == input_data
    assert input_data["a"] + input_data["b"] == input_data["expected"]

def test_subtract(input_data, integration: Integration):
    logging.info("from test test_subtract")
    assert integration.source.user_properties["input_data"] == input_data
    assert integration.destination.user_properties["input_data"] == input_data
    assert input_data["a"] - input_data["b"] == input_data["expected"]
