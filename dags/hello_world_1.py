"""
Concepts: Create DAG, Tasks and Dependencies

A simple dag with 2 tasks of type PythonOperators
task_1 prints "Hello"
task_2 prints "World"
"""

# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
    'owner': 'sankar',
    'start_date': days_ago(1),
    # 'depends_on_past': False,
    # 'email': ['airflow@example.com'],
    # 'email_on_failure': False,
    # 'email_on_retry': False,
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(dag_id='hello_world_1', default_args=default_args, schedule_interval=None)

# hello_task and world_task are examples of tasks created by instantiating operators
def hello_func(**context):
    print("Hello")

hello_task = PythonOperator(
    task_id="hello_task",
    dag=dag,
    python_callable=hello_func,
    provide_context=True
)

def world_func(**context):
    print("World")

world_task = PythonOperator(
    task_id="world_task",
    dag=dag,
    python_callable=world_func,
    provide_context=True
)

hello_task >> world_task