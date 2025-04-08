#!/bin/bash

rm -rf allure-results
mkdir -p allure-results

if [ -d "allure-report/history" ]; then
  cp -r allure-report/history allure-results/history
fi

pytest --data-dir=test_data -n 4 --alluredir=allure-results "$@"

allure generate allure-results -o allure-report --clean
allure open allure-report
