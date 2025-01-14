from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define a function to fetch data using PostgresHook
def fetch_data_from_postgres(**context):
    # Initialize the PostgresHook
    hook = PostgresHook(postgres_conn_id='postgres')

    name = context['params']['name']
    
    # Define your query
    query = f"SELECT * FROM partners WHERE name='{name}' AND execution_date=now()::date-1;"
    print(f"Executing query: {query}")
    
    # Run the query
    connection = hook.get_conn()  # Get a raw connection
    cursor = connection.cursor()
    cursor.execute(query)
    
    # Fetch results
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    # Log or process the results
    for row in results:
        print(f"Name: {row[0]}, Created At: {row[1]}")
    return results

# Define the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='postgres_hook_example_v3',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # Run on demand
) as dag:

    # Define the PythonOperator
    fetch_data_task = PythonOperator(
        task_id='fetch_data_from_postgres',
        python_callable=fetch_data_from_postgres,
        params={'name': 'partner_a'},
    )

    fetch_data_task
