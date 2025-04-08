#!/bin/bash

rm -rf allure-results
rm -rf allure-report
FILE="test_execution.log"

if [ -f "$FILE" ]; then
  #echo "Deleting $FILE..."
  rm "$FILE"
#else
  #echo "File $FILE does not exist. Skipping deletion."
fi