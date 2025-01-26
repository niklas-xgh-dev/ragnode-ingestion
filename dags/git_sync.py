from dotenv import load_dotenv
import git
import os

load_dotenv()

REPO_URL = os.getenv('REPO_URL')
# to differentiate between local testing and prod deployment
IS_AIRFLOW = os.getenv('AIRFLOW_HOME') is not None

def sync_repo():
    repo = git.Repo()
    print(f"Pulling latest changes from {repo.remotes.origin.url}")
    repo.remotes.origin.pull()

if IS_AIRFLOW:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from datetime import datetime

    dag = DAG(
        'github_sync',
        default_args={
            'owner': 'airflow',
            'start_date': datetime(2025, 1, 1)
        },
        schedule_interval='*/5 * * * *',
        catchup=False
    )

    sync_task = PythonOperator(
        task_id='sync_dags',
        python_callable=sync_repo,
        dag=dag
    )
else:
    # Local testing
    sync_repo()
