"""Airflow dag file for extracting, cleaning and transforming cricinfo batters data"""

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from cricinfo_scraper.cricinfo_link_scraper import get_links
from cricinfo_scraper.pandas_scraper import get_all_scorecards
from cricinfo_scraper.batters_cleaning import clean_batters_dataframe
from cricinfo_scraper.batters_totals import batters_totals


dag = DAG(
    dag_id="extract_clean_transform_cricinfo_ipl_data",
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
    links = ti.xcom_pull(key="links", task_ids="get_links")
    df = get_all_scorecards(links)
    df.to_csv("./data/batters.csv")


store_raw_scorecard_csv = PythonOperator(
    task_id="store_raw_scorecard",
    python_callable=_store_raw_scorecard,
    dag=dag,
)


def _store_cleaned_scorecard(ti):
    import pandas as pd

    df: pd.DataFrame = pd.read_csv("./data/batters.csv", index_col="Unnamed: 0")
    df = clean_batters_dataframe(df)
    df.to_csv("./data/batters_cleaned.csv")


store_cleaned_scorecard_csv = PythonOperator(
    task_id="store_cleaned_scorecard",
    python_callable=_store_cleaned_scorecard,
    dag=dag,
)


def _store_batters_totals():
    import pandas as pd

    df = pd.read_csv("./data/batters_cleaned.csv")
    df = batters_totals(df)
    df.to_csv("./data/batters_totals.csv")


store_batters_totals_csv = PythonOperator(
    task_id="store_batters_totals",
    python_callable=_store_batters_totals,
    dag=dag,
)


notify = BashOperator(
    task_id="notify",
    bash_command='echo "The cricinfo tables have been stored"',
    dag=dag,
)

(
    get_ipl_links
    >> store_raw_scorecard_csv
    >> store_cleaned_scorecard_csv
    >> store_batters_totals_csv
    >> notify
)
