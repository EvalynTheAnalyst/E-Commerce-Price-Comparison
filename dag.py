# Automate the process using airflow
from airflow import DAG 
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from web_scraping import scrape_jumia, save_to_data

def run_scrape():
   save_to_data()

default_args = {  
   'owner': 'Eva',
   'email':['evelynnjagi01@gmail.com'],
   'retries': 2,
   'retry_delay': timedelta(minutes=2)
}

with DAG(
   dag_id='price_track_dag',
   default_args=default_args,
   start_date=datetime(2025,6,7),
   description='Jumia phone price scrapping automation',
   schedule_interval='@daily',
   catchup=False
) as dag:
   
   task1 = PythonOperator(
      task_id='scrape_jumia_data',
      python_callable=run_scrape  
   )

task1

