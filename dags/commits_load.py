from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import logging
import snowflake.connector

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
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
    # Read CSV and load to Snowflake
    def load_csv_to_snowflake():
        # Read CSV file (Assuming the CSV is available locally)
        df = pd.read_csv('/opt/airflow/dags/commits.csv')

        # Convert DataFrame to a list of tuples
        data = list(df.itertuples(index=False, name=None))

        # Prepare Snowflake insert query
        insert_query = """
        INSERT INTO commits (sha, author, date, message)
        VALUES (%s, %s, %s, %s);
        """

        # Use the Snowflake connection to insert data
        from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
        hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
        conn = hook.get_conn()
        cursor = conn.cursor()
        

        # Insert rows one by one
        for row in data:
            cursor.execute(insert_query, row)

        conn.commit()
        cursor.close()
        conn.close()

    # Task to load CSV data
    load_csv_data = PythonOperator(
        task_id='load_csv_to_snowflake',
        python_callable=load_csv_to_snowflake
    )
    
    # Set task dependencies (only one task here)
    load_csv_data
