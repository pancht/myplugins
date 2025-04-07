# without pytest-xdist 
pytest --data-dir=test_data 

# with pytest-xdist
pytest --data-dir=test_data -n 4
