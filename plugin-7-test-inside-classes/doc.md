# without pytest-xdist 
pytest --data-dir=test_data 

# with pytest-xdist
pytest --data-dir=test_data -n 4


# allure reports
pytest --data-dir=test_data -n 4 --alluredir=allure-results

allure serve allure-results
