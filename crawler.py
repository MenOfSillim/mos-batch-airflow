import json
import requests
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from databaseConfig import DBHandler

# DAG 설정
dag = DAG(
    dag_id='test_dag',
    start_date=datetime(2022, 9, 17),
    catchup=False,
    tags=['crawling'],
    schedule_interval='@once')


def send_api(path, method):
    API_HOST = "https://gateway-kw.kakao.com"
    url = API_HOST + path
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        "key1": "value1",
        "key2": "value2"
    }

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))

        print("response status %r" % response.status_code)
        print("response text %r" % response.text)
    except Exception as ex:
        print(ex)
    print('한국말 보고싶어')
    # 이미지는 확장자 webp 붙여야됨
    # 썸네일 이미지 featuredCharacterImageA
    # 썸네일 이미지 featuredCharacterImageB
    resultJson = response.json()
    sections = resultJson['data']['sections']

    for i in sections:
        print(i)


# https://popcorn16.tistory.com/122


def conn_mongo():
    mongo = DBHandler()
    print('=============================== Test ===============================')

    # print(mongo.insert_item_one({"test": 1}, 'crawling', 'webtoon'))
    result = mongo.find_item(None, 'crawling', 'webtoon')
    for a in result:
        print(a)

    print('=============================== Test ===============================')


def http_call():
    print("2번째")


# DAG Task 작성
send_api = PythonOperator(
    task_id='send_api',
    # python_callable param points to the function you want to run
    python_callable=send_api,
    op_args=['/section/v2/pages/rank', 'GET'],
    # dag param points to the DAG that this task is a part of
    dag=dag
)

http_call = PythonOperator(
    task_id='http_call',
    # python_callable param points to the function you want to run
    python_callable=http_call,
    # dag param points to the DAG that this task is a part of
    dag=dag
)

conn_mongo = PythonOperator(
    task_id='conn_mongo',
    python_callable=conn_mongo,
    dag=dag
)

# send_api >> http_call
conn_mongo
