# Basic step to start with Apache Airflow
* Local executor
* Database :: PostgreSQL


## 1. Create Apache Airflow with Docker
* https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Download docker-compose.yml
```
$curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.4/docker-compose.yaml'
```

## 2. Initial folders and users
```
$mkdir -p ./dags ./logs ./plugins ./config
$echo -e "AIRFLOW_UID=$(id -u)" > .env
```

List of folders
- ./dags - you can put your DAG files here.
- ./logs - contains logs from task execution and scheduler.
- ./config - you can add custom log parser or add airflow_local_settings.py to configure cluster policy.
- ./plugins - you can put your custom plugins here.

## 3. Initial database of airflow
* Default = SQLite
* PostgreSQL and Redis

```
$docker compose up airflow-init
```

Check status
```
$docker compose ps  

NAME               IMAGE                COMMAND                  SERVICE    CREATED          STATUS                    PORTS
basic-postgres-1   postgres:13          "docker-entrypoint.s…"   postgres   34 seconds ago   Up 33 seconds (healthy)   5432/tcp
basic-redis-1      redis:7.2-bookworm   "docker-entrypoint.s…"   redis      34 seconds ago   Up 33 seconds (healthy)   6379/tcp
```

User and Password to access Airflow
* user=airflow
* password=airflow


## 4. Delete all resources
```
$docker compose down --volumes --remove-orphans
```

## 5. Start all again
```
$docker compose up -d
$docker compose ps  
```

List of process
* PostgreSQL
* airflow-init
* airflow-triggerer
* airflow-scheduler
* airflow-webserver

Access to Airflow webserver
* http://localhost:8080/

## 6. Delete all
```
$docker compose down --volumes --remove-orphans
```

## 7. Start all again
* Change `AIRFLOW__CORE__LOAD_EXAMPLES: 'false'`
  * Not download example

```
$docker compose up -d
$docker compose ps  
```

## Ready to create DAG !!