"""Airflow dag file for extracting, cleaning and transforming cricinfo batters data"""

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from cricinfo_scraper.cricinfo_link_scraper import get_links
from cricinfo_scraper.pandas_scraper import store_raw_scorecard
from cricinfo_scraper.batters_cleaning import store_cleaned_dataframe
from cricinfo_scraper.batters_totals import store_batters_totals


dag = DAG(
    dag_id="extract, clean and transform cricinfo ipl data",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval=None,
)


def _get_links(ti):
    links = get_links()
    ti.xcom_push(key="links", value=links)


get_ipl_links = PythonOperator(
    task_id="get_links",
    python_callable=_get_links,
    dag=dag,
)


def _store_raw_scorecard(ti):
    links = ti.xcom_pull(key="links", task_ids="get_ipl_links")
    store_raw_scorecard(links)


store_raw_scorecard_csv = PythonOperator(
    task_id="store_raw_scorecard",
    python_callable=_store_raw_scorecard,
    dag=dag,
)


store_cleaned_scorecard_csv = PythonOperator(
    task_id="store_cleaned_scorecard",
    python_callable=store_cleaned_dataframe,
    dag=dag,
)


store_batters_totals_csv = PythonOperator(
    task_id="store_batters_totals",
    python_callable=store_batters_totals,
    dag=dag,
)


notify = BashOperator(
    task_id="notify",
    bash_command='echo "The cricinfo tables have been stored"',
    dag=dag,
)

get_ipl_links >> store_raw_scorecard_csv >> store_cleaned_scorecard_csv >> store_batters_totals_csv >> notify
