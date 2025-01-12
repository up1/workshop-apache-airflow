from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mysql.connector
import random
from datetime import datetime, timedelta

# Define default_args and DAG
default_args = {
    'owner': 'demo-user',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'website_traffic_etl',
    default_args=default_args,
    description='ETL process for website traffic data',
    schedule_interval=timedelta(minutes=1),  # Run every a minutes
    catchup=False,
)

# ETL Function
def etl():
    connection = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="mydb"
    )
    cursor = connection.cursor()
    
    # Generate and insert synthetic data
    timestamp = datetime.now()
    pageviews = random.randint(100, 1000)
    unique_visitors = random.randint(50, 200)
    cursor.execute("INSERT INTO traffic (timestamp, pageviews, unique_visitors) VALUES (%s, %s, %s)",
                   (timestamp, pageviews, unique_visitors))
    
    # Commit changes and close the connection
    connection.commit()
    connection.close()

# Define the ETL task
etl_task = PythonOperator(
    task_id='etl_task',
    python_callable=etl,
    dag=dag,
)

# Set task dependencies
etl_task
