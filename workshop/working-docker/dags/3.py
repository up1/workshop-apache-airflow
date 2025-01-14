import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import json
import requests

def parse_json(file_path):
    with open(file_path) as f:
        albums = json.load(f)
        for album in albums:
            print(f"Downloading for album {album['id']}")
            download_image_from_albums(album['id'])

def download_image_from_albums(album_id) -> str:
    response = requests.get(f'https://jsonplaceholder.typicode.com/albums/{album_id}/photos')
    with open(f'/opt/airflow/logs/{album_id}.json', 'w') as f:
        json.dump(response.json(), f)

with DAG(
    dag_id="workshop_01_v8",
    description="First workshop",
    start_date=pendulum.today("UTC").add(days=-5),
    schedule="@daily",
    catchup=False,
):
    task1 = BashOperator(
        task_id="task1", 
        bash_command="curl -o /opt/airflow/logs/albums.json -L 'https://jsonplaceholder.typicode.com/albums'")

    task2 = PythonOperator(
        task_id="task2",
        python_callable=parse_json,
        op_args=["/opt/airflow/logs/albums.json"],
    )

    task3 = EmptyOperator(task_id="task3")

    task1 >> task2 >> task3