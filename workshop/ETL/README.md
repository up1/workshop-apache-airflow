# ETL workshop
* Data pipeline with Apache Airflow
* Database = MySQL
* Visualization = Apache Superset


## 1. Create MySQL database
```
$docker compose up -d mysql
$docker compose ps
```

## 2. Create Superset
```
$docker compose up -d superset --build
$docker compose ps
```

### Initial data
```
// Access to container
$docker exec -it superset /bin/bash

// Create user
$superset fab create-admin --username admin --firstname superset --lastname Admin --email admin@superset.com --password XXXX

// Upgrade database
$superset db upgrade

// Initial superset
$superset init
```

Access to dashboard
* http://localhost:8088
  * Go to Settings -> Database connections
    * Add connection for MySQL
      * mysql://user:password@mysql:3306/mydb
        * database=mydb
        * username=user
        * password=password


## 3. Initial data for test
* Random data
```
$pip install -r requirements.txt
$python 1-setup-data.py
```

## 4. Create dashboard in Superset

Access to dashboard
* http://localhost:8088

## 5. DAG with Apache Airflow
```
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
```
### Clear all
```
$docker builder prune
```

### Reference Websites
* https://superset.apache.org/docs/configuration/databases/
