from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task
from datetime import datetime

dag = DAG(
    'trigger_dag_with_params_v2',
    schedule_interval='@daily', 
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["example"],
    params={
        "param1": "Hello",
        "param2": "Airflow!",
    },
)

task1 = EmptyOperator(task_id='task1', dag=dag)

@task
def task2(**context):
    print(context["params"]["param1"], context["params"]["param2"])

task1 >> task2()