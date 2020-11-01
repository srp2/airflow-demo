"""
Concepts: Branching in workflow

A simple dag with 2 tasks of type PythonOperators
task_1 pushes {"task1_value": "Hello"} into xcom
task_2 retrives task1_value (i.e. Hello ) from xcom
adds string " World" to it and prints it
"""

from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
import datetime

default_args={
    'owner': 'sankar',
    'start_date': days_ago(1)
}

dag = DAG(
    dag_id='branch_workflow_6',
    default_args=default_args,
    description='Branching in workflow',
    schedule_interval=None)

def begin_func(**context):
    print('Beginning of workflow')

task_begin = PythonOperator(
    task_id='task_begin',
    dag=dag,
    python_callable=begin_func,
    provide_context=True
)

def end_func(**context):
    print('End of workflow')

task_end = PythonOperator(
    task_id='task_end',
    dag=dag,
    python_callable=end_func,
    provide_context=True,
    trigger_rule='one_success'
)

def branch_func(**context):
    second = datetime.datetime.now().second
    sec_mod_5 = str(second % 5)
    return 'task_' + sec_mod_5

task_branch = BranchPythonOperator(
    task_id='branching',
    dag=dag,
    python_callable=branch_func,
    provide_context=True
)

task_begin >> task_branch

for task in range(5):
    t = DummyOperator(
        task_id='task_'+str(task),
        dag=dag,
    )

    task_branch >> t >> task_end