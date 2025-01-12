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

// Install MySQL
$pip install mysqlclient
```

Access to dashboard
* http://localhost:8088
  * Go to Settings -> Database connections
    * Add connection for MySQL
      * mysql://user:password@mysql:3306/mydb
        * database=mydb
        * username=user
        * password=password


## 3. DAG with Apache Airflow
* TODO




### Clear all
```
$docker builder prune
```