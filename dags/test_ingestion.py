from common.database import Session
from common.models import ChatMessage, BadenRAG
import os
from dotenv import load_dotenv

load_dotenv()

IS_AIRFLOW = os.getenv("AIRFLOW_HOME") is not None

def test_ingestion():
    with Session() as session:
        data = ChatMessage(role = "test", content="This is just a test message")
        session.add(data)
        session.commit()

if IS_AIRFLOW:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    with DAG('test_ingestion', 
            schedule_interval='*/5 * * * *',
            catchup=False) as dag:
        
        PythonOperator(task_id='sync_dags', python_callable=test_ingestion)

else:
    test_ingestion()