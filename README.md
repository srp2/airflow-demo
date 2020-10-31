# airflow-demo

https://github.com/puckel/docker-airflow

copy https://github.com/puckel/docker-airflow/blob/master/docker-compose-LocalExecutor.yml to local file docker-compose.yml

docker-compose up
* number of DAGs, url
* version, DAG

hello_world_1
* UI, pause, tree view, graph view

hello_world_xcom_2
* log/xcom
* postgres

restart_failed_task_3
auto_restart_failed_task_4

Trigger via REST

curl -X POST \
http://localhost:8080/api/experimental/dags/<DAG_ID>/dag_runs \
-H 'Cache-Control: no-cache' \
-H 'Content-Type: application/json' \
-d '{"conf":"{\"key\":\"value\"}"}'

curl -X POST \
http://localhost:8080/api/experimental/dags/hello_world_1/dag_runs \
-H 'Cache-Control: no-cache' \
-H 'Content-Type: application/json' \
-d '{}'


trigger_dag_rest_pass_value_5 
Trigger via REST and pass run time configuration
curl -X POST \
http://localhost:8080/api/experimental/dags/trigger_dag_rest_pass_value_5/dag_runs \
-H 'Cache-Control: no-cache' \
-H 'Content-Type: application/json' \
-d '{"conf":"{\"key1\":\"A Beautiful\", \"key2\":\"Not used\"}"}'

Trigger via REST and pass run time configuration and run_id
curl -X POST \
http://localhost:8080/api/experimental/dags/trigger_dag_rest_pass_value_5/dag_runs \
-H 'Cache-Control: no-cache' \
-H 'Content-Type: application/json' \
-d '{"conf":"{\"key1\":\"A Beautiful\", \"key2\":\"Not used\"}", "run_id": "my_awesome_run"}'


Docker remove all containers
docker rm -vf $(docker ps -a -q)

remove all images
docker rmi -f $(docker images -a -q)