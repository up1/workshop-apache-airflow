FROM apache/superset
USER root
RUN apt-get update -y
RUN apt install -y pkg-config  default-libmysqlclient-dev build-essential
RUN pip install mysqlclient
USER superset