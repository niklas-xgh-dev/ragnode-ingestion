from dotenv import load_dotenv
import git
import os

load_dotenv()

REPO_URL = os.getenv('REPO_URL')
IS_AIRFLOW = os.getenv('AIRFLOW_HOME') is not None
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', './dags')  # Fallback to local dir

def sync_repo():
    try:
        repo = git.Repo(f'{AIRFLOW_HOME}/dags')
        repo.remotes.origin.pull()
    except git.exc.InvalidGitRepositoryError:
        git.Repo.clone_from(REPO_URL, f'{AIRFLOW_HOME}/dags')

if IS_AIRFLOW:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from datetime import datetime

    dag = DAG(
        'github_sync',
        default_args={
            'owner': 'airflow',
            'start_date': datetime(2024, 1, 1)
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