from airflow import DAG
from airflow.providers.google.common.hooks.base_google import GoogleBaseHook
import pandas as pd
from pendulum import now
import gspread
from datetime import datetime


with DAG(
    dag_id="save_data_to_spreadsheet_v8",
    start_date=datetime.now(),
    schedule_interval="@daily",
) as dag:

    @dag.task
    def data_to_spreadsheet_task():
        data = {
            "tasks": ["task 01", "task 02", "task 03"],
            "date": ["2025-01-01", "2025-01-02", "2025-01-03"],
        }

        df = pd.DataFrame(data)

        # Hook to Google Sheets in order to get connection from Airflow
        hook = GoogleBaseHook(gcp_conn_id="google_conn_id")
        credentials = hook.get_credentials()
        google_credentials = gspread.Client(auth=credentials)

        # Reading a spreadsheet by its title
        sheet = google_credentials.open("tasks-list-2025")

        # Defining the worksheet to manipulate
        worksheet = sheet.worksheet("tasks")

        # Sending data from df to the worksheet and appending it
        worksheet.append_rows(df.values.tolist())

    @dag.task
    def read_spreadsheet_task():
        hook = GoogleBaseHook(gcp_conn_id="google_conn_id")
        credentials = hook.get_credentials()
        google_credentials = gspread.Client(auth=credentials)

        # Reading a spreadsheet by its title
        sheet = google_credentials.open("tasks-list-2025")

        # Defining the worksheet to manipulate
        worksheet = sheet.worksheet("tasks")

        # Reading data from the worksheet
        data = worksheet.get_all_values()
        print(data)

    data_to_spreadsheet_task() >> read_spreadsheet_task()