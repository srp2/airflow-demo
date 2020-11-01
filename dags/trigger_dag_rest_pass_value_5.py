"""
Concepts: Trigger DAG via REST endpoint

A simple dag with 2 tasks of type PythonOperators
task_1 received the runtime config from curl and
pushes key1 value into xcom {"task1_value": val1}
task_2 retrives task1_value (i.e. Hello ) from xcom
adds string " World" to it and prints it
"""

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

default_args={
    'owner': 'sankar',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='trigger_dag_rest_pass_value_5',
    default_args=default_args,
    description='Trigger DAG via REST endpoint',
    schedule_interval=None)

# https://airflow.apache.org/docs/stable/rest-api-ref.html#post--api-experimental-dags--DAG_ID--dag_runsS
# https://github.com/apache/airflow/blob/master/airflow/www/api/experimental/endpoints.py
def task1_func(**context):
    # Print the payload passed to the DagRun conf attribute.
    print(context['dag_run'].conf)
    val1 = context['dag_run'].conf['key1']
    context['ti'].xcom_push(key='task1_value', value=val1)
    print('task1_complete')

task1 = PythonOperator(
    task_id='task_1',
    dag=dag,
    python_callable=task1_func,
    provide_context=True
)

def task2_func(**context):
    msg = context['ti'].xcom_pull(key='task1_value') + ' World!!'
    print(msg)

task2 = PythonOperator(
    task_id='task_2',
    dag=dag,
    python_callable=task2_func,
    provide_context=True
)

task1 >> task2