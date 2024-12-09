from airflow import DAG
from datetime import datetime
import os
import sys

from pipelines.reddit_pipeline import reddit_pipeline
from pipelines.upload_s3_pipeline import upload_s3_pipeline

from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

default_args = {
    'owner' : 'Misael',
    'start_date' : datetime(2024, 12, 4)
}

file_postfix = datetime.now().strftime('%Y%m%d')

dag = DAG(
    dag_id = 'reddit_dag',
    default_args = default_args,
    schedule_interval = '@daily',
    catchup= False,
    tags = ['reddit', 'etl']
)

## Extraction from Reddit

extract = PythonOperator(
    task_id = 'reddit_extraction',
    python_callable = reddit_pipeline,
    op_kwargs = {
        'file_name' : f'reddit_{file_postfix}',
        'subreddit' : 'dataengineering',
        'time_filter' : 'day',
        'limit' : 100
    },
    dag = dag
)

## Uploading to S3

upload_s3 = PythonOperator(
    task_id = 's3_upload',
    python_callable = upload_s3_pipeline,
    dag = dag
)

## order execution

extract >> upload_s3