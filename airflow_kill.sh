#!/bin/bash

# Get all airflow process IDs except the grep process itself
# and kill them with -9
ps aux | grep airflow | grep -v grep | awk '{print $2}' | xargs -r kill -9

# Print confirmation
echo "All Airflow processes killed"