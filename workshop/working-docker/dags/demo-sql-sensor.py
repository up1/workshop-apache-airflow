from airflow.decorators import task, dag
from airflow.sensors.sql import SqlSensor

from typing import Dict
from datetime import datetime

def _success_criteria(record):
    return record

def _failure_criteria(record):
    return True if not record else False

@dag(dag_id='partner_v4',
     description='DAG in charge of processing partner data',
     start_date=datetime(2025, 1, 1), 
     schedule_interval='@daily',
     catchup=False)

def partner():
    waiting_for_partner = SqlSensor(
        task_id='waiting_for_partner',
        conn_id='postgres',
        sql='sql/check.sql',
        parameters={
            'name': 'partner_a'
        },
        success=_success_criteria,
        failure=_failure_criteria,
        fail_on_empty=False,
        poke_interval=20, # check every 20 seconds
        mode='reschedule',
        timeout=60 * 5
    )
    
    @task
    def validation() -> Dict[str, str]:
        return {'partner_name': 'partner_a', 'partner_validation': True}
    
    @task
    def storing(**context):
        context = context['task_instance']
        partner_name = context.xcom_pull(task_ids='validation')['partner_name']
        partner_validation = context.xcom_pull(task_ids='validation')['partner_validation']
        print(f"Storing partner {partner_name} with validation {partner_validation}")
        
    
    waiting_for_partner >> validation() >> storing()
    
dag = partner()