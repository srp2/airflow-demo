"""
Concepts: Auto restart of failed task

task1:
if random >= 0.7 raise exception
else push {"task1_value": "Hello"} into xcom
task_2:
retrives task1_value (i.e. Hello ) from xcom
adds string " World" to it and prints it
"""

from airflow.models import DAG
from airflow.utils.dates import days_ago, timedelta
from airflow.operators.python_operator import PythonOperator
import random

default_args={
    'owner': 'sankar',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='auto_restart_failed_task_4',
    default_args=default_args,
    description='Auto restart of failed task',
    schedule_interval=None)

def task1_func(**context):
    # random floating point number in the range [0.0, 1.0)
    if random.random() >= 0.7:
        raise Exception('task_1 exception')
    else:
        context['ti'].xcom_push(key='task1_value', value='Hello')
    print("task1_complete")

"""
    https://airflow.apache.org/docs/stable/_modules/airflow/models/baseoperator.html
    :param retries: the number of retries that should be performed before failing the task
    :type retries: int
    :param retry_delay: delay between retries
    :type retry_delay: datetime.timedelta
"""
task1 = PythonOperator(
    task_id="task_1",
    dag=dag,
    python_callable=task1_func,
    provide_context=True,
    retries=10,
    retry_delay=timedelta(seconds=5)
)

def task2_func(**context):
    msg = context['ti'].xcom_pull(key='task1_value') + ' World!!'
    print(msg)

task2 = PythonOperator(
    task_id="task_2",
    dag=dag,
    python_callable=task2_func,
    provide_context=True
)

task1 >> task2