"""
Mock ingestion DAG for testing and development.
"""
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

IS_AIRFLOW = os.getenv('AIRFLOW_HOME') is not None

# DAG configuration
default_args = {
    'owner': 'ragnode',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
    'max_active_runs': 1
}

def fetch_mock_data(**context):
    """Simulate fetching data from a source."""
    print("Fetching mock data...")
    return {
        "timestamp": datetime.now().isoformat(),
        "documents": [
            {"id": 1, "content": "Mock document 1"},
            {"id": 2, "content": "Mock document 2"}
        ]
    }

def process_mock_data(**context):
    """Process the mock data."""
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='fetch_data')
    print(f"Processing {len(data['documents'])} documents...")
    
    # Add mock vectors
    for doc in data['documents']:
        doc['vector'] = [0.1, 0.2, 0.3]  # Mock embedding
    
    return data

def store_mock_data(**context):
    """Mock storing the data."""
    ti = context['task_instance']
    data = ti.xcom_pull(task_ids='process_data')
    print(f"Would store {len(data['documents'])} documents")

if IS_AIRFLOW:
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    # Define the DAG
    with DAG(
        'mock_ingestion',
        default_args=default_args,
        description='Mock data ingestion pipeline',
        schedule_interval=timedelta(minutes=5),
        catchup=False
    ) as dag:

        fetch_data = PythonOperator(
            task_id='fetch_data',
            python_callable=fetch_mock_data
        )

        process_data = PythonOperator(
            task_id='process_data',
            python_callable=process_mock_data
        )

        store_data = PythonOperator(
            task_id='store_data',
            python_callable=store_mock_data
        )

        # Set dependencies
        fetch_data >> process_data >> store_data

else:
   # Simulate Airflow context for local testing
   context = {'task_instance': type('MockTaskInstance', (), {
       'xcom_pull': lambda task_ids: mock_data.get(task_ids)
   })}
   
   mock_data = {}
   mock_data['fetch_data'] = fetch_mock_data(**context)
   mock_data['process_data'] = process_mock_data(**context) 
   store_mock_data(**context)