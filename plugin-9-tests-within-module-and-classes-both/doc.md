# without pytest-xdist 
pytest --data-dir=test_data 

# with pytest-xdist
pytest --data-dir=test_data -n 4






# allure reports
## Save the above steps in a shell script like run_tests.sh:
run_test.sh
-----------
#!/bin/bash

rm -rf allure-results
mkdir -p allure-results

if [ -d "allure-report/history" ]; then
  cp -r allure-report/history allure-results/history
fi

pytest tests/ --alluredir=allure-results "$@"

allure generate allure-results -o allure-report --clean
allure open allure-report

## Make it executable:
chmod +x run_tests.sh

## Run via:
./run_tests.sh
