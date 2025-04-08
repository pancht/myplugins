#!/bin/bash

rm -rf allure-results
mkdir -p allure-results

if [ -d "allure-report/history" ]; then
  cp -r allure-report/history allure-results/history
fi
# run tests with allure
pytest --data-dir=test_data -n 4 --alluredir=allure-results "$@"
# overwrite categories.json
cp .allure/categories.json allure-results/categories.json
# generate allure results
allure generate allure-results -o allure-report --clean
# open allure report (optional)
allure open allure-report
