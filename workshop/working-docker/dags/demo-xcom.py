from datetime import datetime
import uuid
from airflow import DAG
from airflow.operators.python import PythonOperator

def _called_task_a(**context):
    product_id = str(uuid.uuid4())
    context["task_instance"].xcom_push(key="product_id", value=product_id)
 
def _called_task_b(**context):
    product_id = context["task_instance"].xcom_pull(key="product_id")
    print(product_id)

with DAG(
    dag_id='demo_xcom_v3',
    start_date=datetime(2025, 1, 1),
    schedule_interval='* * * * *',
    catchup=False,
) as dag:

    task_a = PythonOperator(
        task_id="task_a", 
        python_callable=_called_task_a,
    )

    task_b = PythonOperator(
        task_id="task_b",
        python_callable=_called_task_b,
    )
    
    task_a >> task_b