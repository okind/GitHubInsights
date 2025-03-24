from airflow import DAG

from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

from airflow.operators.python import PythonOperator

from airflow.models import Variable

import datetime

import pandas as pd

import logging

from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

import commitsJobHandler
from dotenv import load_dotenv
import os


# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2024, 1, 1),
    'retries': 1
}

# Define the DAG
with DAG(
    'csv_to_snowflake',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
) as dag:

     logging.basicConfig(level=logging.DEBUG)

    # Fetch commits data from GitHub and save it to a CSV file commits.csv
    def extract_github_commits(*args):

        # Read the token from the airflow variable
        github_token = Variable.get("GITHUB_TOKEN")

        logging.info('GitHub token provided = %s', github_token != None)

        REPO_OWNER = args[0]
        REPO_NAME = args[1]
        commitsJobHandler.extract_commits_data(
            REPO_OWNER, REPO_NAME, github_token)

    # Read commits.csv and load commits to Snowflake
    def load_csv_to_snowflake():

        # Read CSV file into a DataFrame
        df = pd.read_csv('/opt/airflow/dags/commits.csv')

        # Convert DataFrame to a list of tuples
        data = list(df.itertuples(index=False, name=None))

        # Prepare Snowflake insert query
        insert_query = """
        INSERT INTO commits (sha, author, date, message, additions, deletions, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        # Use the Snowflake connection to insert data
        hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Insert rows one by one
        for row in data:
            cursor.execute(insert_query, row)

        conn.commit()
        cursor.close()
        conn.close()

    # Task to extract data from repo 'Scraping-Youtube-Comments' in 'dddat1017' account to commits.csv
    extract_data = PythonOperator(
        task_id='extract_data_from_github',
        op_args=['dddat1017', 'Scraping-Youtube-Comments', None],
        python_callable=extract_github_commits
    )
    # Task to load commits data to Snowflake
    load_csv_data = PythonOperator(
        task_id='load_csv_to_snowflake',
        python_callable=load_csv_to_snowflake
    )

    # Set task dependencies for the DAG
    extract_data >> load_csv_data
