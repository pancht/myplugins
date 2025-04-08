#!/bin/bash

rm -rf allure-results
mkdir -p allure-results

# Copy custom categories
cp .allure/categories.json allure-results/categories.json

if [ -d "allure-report/history" ]; then
  cp -r allure-report/history allure-results/history
fi
# run tests with allure
pytest --data-dir=test_data -n 4 --alluredir=allure-results "$@"
# generate allure results
allure generate allure-results -o allure-report --clean
# open allure report (optional)
allure open allure-report
