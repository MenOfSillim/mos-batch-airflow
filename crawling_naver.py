import datetime
from crawler.naver import do_crawling
from airflow import DAG
from airflow.operators.python import PythonOperator

from config.database_config import DBHandler

# DAG 설정
dag = DAG(
    dag_id='dag_crawling_naver',
    start_date=datetime.datetime(2022, 9, 17),
    catchup=False,
    tags=['crawling'],
    schedule_interval='@once')


def crawling_naver(start_index, end_index):
    print('=============================== Crawling Start ===============================')
    print(start_index)
    print(end_index)
    # mongo = DBHandler('crawling', 'webtoon')
    do_crawling()
    print('=============================== Crawling End ===============================')


# DAG Task 작성
crawling_naver = PythonOperator(
    task_id='task_crawling_naver',
    # python_callable param points to the function you want to run
    python_callable=crawling_naver,
    op_args=[0, 100],
    # dag param points to the DAG that this task is a part of
    dag=dag
)

crawling_naver
