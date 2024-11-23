# GitHub Insights Project on Open Source Technologies

GitHub Insights is a feature within GitHub Enterprise that provides organizations with detailed analytics and
 insights into their codebase, team productivity, and workflows. It offers a data-driven view of a project’s development health,
 which can help teams optimize performance, identify bottlenecks, and make informed decisions.

## Key Features
### Team Productivity
- Measures contributions across team members, including volume and frequency,
  allows managers to understand team dynamics and work distribution.


---

## Key Components of the Project

### Docker
1. **Docker Compose**:
    - A `docker-compose.yml` file defines how each service (Airflow, dbt, etc.) interacts.
    - Allows consistent setup and easy deployment of the ETL pipeline across environments.
2. Airflow, Snowflake connectors, and other ETL dependencies can run inside Docker containers.

---

### Airflow (Orchestration)
1. Airflow is used to **schedule** and manage the entire ETL process by managing dependencies between tasks.
2. An Airflow DAG (Directed Acyclic Graph) is created to define the workflow steps.
    - The DAG defines the sequence (e.g., Extract → Transform → Load) and schedules when each task should run.

---

### dbt (Data Build Tool)
- Handles transformation of raw data into the desired structure, applying **business logic**.
- Builds SQL transformations on top of raw tables, generating models and views in **Snowflake**.
- Process:
  1. Create a dbt project where you define models, schema tests, and transformation logic.
  2. Materialize models as tables or views in Snowflake.

---

### Snowflake
1. **Scalable cloud data storage** platform.
2. Steps:
   - Create a table and define its structure.
   - Table structure includes:
     - `SHA` (Secure Hash Algorithm): Represents unique commit identifier.
     - `Author`: Commit author.
     - `Date`: Commit date.
     - `Message`: Commit message, serve as documentation, explaining why changes were made and their impact.

---

## Project Workflow
1. **Extract**: 
    - Airflow extracts data from the CSV file and temporarily stores it.
2. **Load (Raw Data)**: 
    - Load extracted raw CSV data into a Snowflake staging table.
3. **Transform (dbt)**: 
    - Transform raw data using SQL models, applying business logic.
4. **Load (Final Data)**: 
    - Load transformed data into a final Snowflake table.
5. **Visualize**: Use tools like Tableau for visualization.

---

## Project Execution Steps

### Step 1: Extract
- The `commitsJobHandler.py` extracts data from a GitHub repository and temporarily stores it in a CSV file.
- Created project folder: `GitHubInsights`.

---

### Step 2: Load
#### Docker Setup
1. Installed Docker Desktop.
2. Downloaded `docker-compose.yaml` file:
    ```bash
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.3/docker-compose.yaml'
    ```
3. **Run Apache Airflow with Docker Compose**:
    - Ensure Docker is installed:
        ```bash
        docker --version
        docker-compose --version
        ```
    - Navigate to the directory with `docker-compose.yaml`:
        ```bash
        cd /path/to/your/docker-compose-file
        ```
    - Start services:
        ```bash
        docker-compose up -d
        ```
    - Access Airflow UI: [http://localhost:8080](http://localhost:8080)
      - Default credentials:
        - Username: `airflow`
        - Password: `airflow`
    - Stop services:
        ```bash
        docker-compose down
        ```

4. **Folder Mapping in Docker Compose**:
    ```yaml
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
      - ./dbt:/dbt
    ```

5. Use Docker Desktop Terminal to verify mappings:
    ```bash
    cd /dbt
    ```

#### Snowflake Setup
1. Create Snowflake connection in Airflow UI (`Admin -> Connections`).
    - Created user `AIRFLOW_ETL` and role `ETL_USER` in Snowflake.
    - Permissions:
        ```sql
        GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ETL_USER;
        GRANT USAGE ON DATABASE COMMITS TO ROLE ETL_USER;
        GRANT USAGE ON SCHEMA COMMITS.PUBLIC TO ROLE ETL_USER;
        GRANT INSERT, SELECT ON TABLE COMMITS.PUBLIC.COMMITS TO ROLE ETL_USER;
        ```

2. Create Snowflake database (`commits`), schema (`public`), and table (`commits`):
    ```sql
    CREATE OR REPLACE TABLE COMMITS.PUBLIC.COMMITS (
        SHA VARCHAR(16777216),
        AUTHOR VARCHAR(16777216),
        DATE DATE,
        MESSAGE VARCHAR(16777216)
    );
    ```

---
## TO DO
### Step 3: Transform
- Use dbt to transform data and load into Snowflake.

---

### Step 4: Visualize
- Created visualizations in **Tableau**.
  ![Screenshot 2024-11-22 at 17 49 59](https://github.com/user-attachments/assets/20f51968-4be9-4069-8bc8-16aff042a867)


---
## TO DO
### Step 5: Automate
- Automated data ingestion to upload only changes.
```
