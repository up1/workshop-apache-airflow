from airflow.decorators import task, dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime


@dag(dag_id='partner_insert',
     description='Insert partner data to database',
     start_date=datetime(2025, 1, 1), 
     schedule_interval='@daily')

def initial_data():
    drop_table = PostgresOperator(
        task_id='drop_table',
        sql='sql/drop_table.sql',
        postgres_conn_id='postgres'
    )
    create_table = PostgresOperator(
        task_id='create_table',
        sql='sql/create_table.sql',
        postgres_conn_id='postgres'
    )

    insert_data = PostgresOperator(
        task_id='insert_data',
        sql='sql/insert_data.sql',
        postgres_conn_id='postgres'
    )

    drop_table >> create_table >> insert_data
    
dag = initial_data()