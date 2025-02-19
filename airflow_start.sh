#!/bin/bash

AIRFLOW_HOME="/home/ansible/airflow"
VENV_PATH="$AIRFLOW_HOME/.venv"

# Deactivate any existing virtualenv
deactivate 2>/dev/null || true

# Ensure PYTHONPATH is clean
unset PYTHONPATH

# Set environment
export AIRFLOW_HOME
export VIRTUAL_ENV="$VENV_PATH"
export PATH="$VENV_PATH/bin:$PATH"

# Start services using absolute paths
"$VENV_PATH/bin/airflow" webserver --daemon --stdout "$AIRFLOW_HOME/airflow-webserver.out" --stderr "$AIRFLOW_HOME/airflow-webserver.err"
"$VENV_PATH/bin/airflow" scheduler --daemon --stdout "$AIRFLOW_HOME/airflow-scheduler.out" --stderr "$AIRFLOW_HOME/airflow-scheduler.err"