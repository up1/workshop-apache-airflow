import uuid
import pendulum
from airflow.decorators import task, dag

@dag( 
    dag_id="demo_dag_decorator_v2",
    start_date=pendulum.today("UTC").add(days=-3),
    schedule="@daily",
)
def taskflow_api_decorator(): 

    @task 
    def task_a():
        product_id = str(uuid.uuid4())
        return product_id

    @task 
    def task_b(product_id: str):
        print(f"Data of product id = {product_id}")

    product_id = task_a()
    task_b(product_id)

taskflow_api_decorator()