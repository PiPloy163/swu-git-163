# [START tutorial]
# [START import_module]
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

with DAG(
    'PiPloy',
    default_args={
		"depends_on_past": False,
		"email": ["pornpimon.srt@g.swu.ac.th"],
		"email_on_failure" : False,
		"email_on_retry" : False,
		"retries" : 1,
		"retry_delay" : timedelta(minutes = 5),},
    description='A simple tutorial DAG',
    schedule = None,
    start_date=datetime(2021, 1, 1),
    tags=['example'],
) as dag:
	t1 = BashOperator(
        	task_id='print_date',
        	bash_command='date',
    )
	t2 = BashOperator(
        	task_id='print_date2',
        	bash_command='date',
    )
 
	t1 >> t2
	def dummy_test():
		return 'branch_a'

	A_task = DummyOperator(task_id='branch_a', dag=dag)
	B_task = DummyOperator(task_id='branch_false', dag=dag)

	branch_task = BranchPythonOperator(
		task_id='branching',
		python_callable=dummy_test,
		dag=dag,
	)

	branch_task >> A_task 
	branch_task >> B_task