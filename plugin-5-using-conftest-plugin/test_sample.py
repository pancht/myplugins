

def test_add(input_data):
    assert input_data["a"] + input_data["b"] == input_data["expected"]

def test_subtract(input_data):
    assert input_data["a"] - input_data["b"] == input_data["expected"]
