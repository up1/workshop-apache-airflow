from pendulum import datetime
from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

DATA = Dataset("/opt/airflow/logs/mydata.txt")


def read_text_data():
    results = []
    with open("/opt/airflow/logs/mydata.txt", "r") as f:
        contents = f.readlines()
        results.append(contents)
    return results



with DAG(
  dag_id="datasets_producer_dag_v6",
  start_date=datetime(2025, 1, 1),
  schedule='@daily',
):
  start_task = BashOperator(
    task_id="start_task",
    bash_command="echo 'Start task'",
    outlets=[DATA],
  )


with DAG(
    dag_id="datasets_consumer_dag_v6",
    start_date=datetime(2025, 1, 1),
    schedule=[DATA],  # Scheduled on Dataset
    catchup=False,
):
    start = PythonOperator(
        task_id="read_data",
        python_callable=read_text_data,
    )

    start