from datetime import datetime
from crawler.kakao_page import do_paraller_crawler
from airflow import DAG
from airflow.operators.python import PythonOperator

from config.database_config import DBHandler

# DAG 설정
dag = DAG(
    dag_id='dag_crawling_kakao_page',
    start_date=datetime(2022, 9, 17),
    catchup=False,
    tags=['crawling'],
    schedule_interval='@once')


def crawling_kakao_page(start_index, end_index):
    print('=============================== Crawling Start ===============================')
    mongo = DBHandler('crawling', 'webtoon')
    # mongo.insert_item_many(do_paraller_crawler(0, 100))
    # mongo.insert_item_many(do_paraller_crawler(100, 200))
    # mongo.insert_item_many(do_paraller_crawler(200, 300))
    # mongo.insert_item_many(do_paraller_crawler(300, 400))
    # mongo.insert_item_many(do_paraller_crawler(400, 543))
    print('=============================== Crawling End ===============================')


# DAG Task 작성
crawling_kakao_page = PythonOperator(
    task_id='task_crawling_kakao_page',
    # python_callable param points to the function you want to run
    python_callable=crawling_kakao_page,
    op_args=[0, 100],
    # dag param points to the DAG that this task is a part of
    dag=dag
)

crawling_kakao_page
