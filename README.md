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
- Created project folder: `GitHubInsights`. Initially it runs manually. 

---

### Step 2: Load
#### Docker Setup
1. Installed Docker Desktop.
2. Downloaded `docker-compose.yaml` file:
    ```bash
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.3/docker-compose.yaml'
    ```
    Set Folder Mapping in Docker Compose:
    ```yaml
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
      - ./dbt:/dbt
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
    - Create a connector to Snowflake. Follow Airflow UI, Admin -> Add Connection, for Connection Type choose Snowflake.
    - Stop services:
        ```bash
        docker-compose down
          ```
     


5. **Use Docker Desktop Terminal to verify mappings**:
    ```bash
    cd /dbt
    ```
6. **Create Snowflake connection in Airflow UI (`Admin -> Connections`, 'Connection Type - Snowflake')**
   ```
   {
     "account: "SPECIFY_YOUR_ACCOUNT_IN_SNOWFLAKE",
     "warehouse": "COMPUTE_WH",
     "database": "COMMITS" ,
     "role": "ETL_USER",
     "insecure mode: False)
    }
   ```

#### Snowflake Setup
1. Create in Snowflake
    - User `AIRFLOW_ETL`
    - Role `ETL_USER` 
    - Permissions:
        ```sql
        GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ETL_USER;
        GRANT USAGE ON DATABASE COMMITS TO ROLE ETL_USER;
        GRANT USAGE ON SCHEMA COMMITS.PUBLIC TO ROLE ETL_USER;
        GRANT INSERT, SELECT ON TABLE COMMITS.PUBLIC.COMMITS TO ROLE ETL_USER;
        ```

3. Create Snowflake database (`commits`), schema (`public`), and table (`commits`):
    ```sql
    CREATE OR REPLACE TABLE COMMITS.PUBLIC.COMMITS (
        SHA VARCHAR(16777216),
        AUTHOR VARCHAR(16777216),
        DATE DATE,
        MESSAGE VARCHAR(16777216)
    );

    ALTER TABLE COMMITS.PUBLIC.COMMITS
    ADD (
    ADDITIONS NUMBER,
    DELETIONS NUMBER,
    TOTAL NUMBER
    );

    Final commits table definition
    create or replace TABLE COMMITS.PUBLIC.COMMITS (
	SHA VARCHAR(16777216),
	AUTHOR VARCHAR(16777216),
	DATE DATE,
	MESSAGE VARCHAR(16777216),
	ADDITIONS NUMBER(38,0),
	DELETIONS NUMBER(38,0),
	TOTAL NUMBER(38,0)
    );
    ```
#### Initial Commits Import
1. **commitsJobHandler.py**
   - Using wrapper around GitHub API githubClient load commit to CSV File, commits.csv.
2. **commits_load.py**
   - Define DAG 'csv_to_snowflake' that imports commits data from commits.csv to Snowflake database commits. 
3. Run Dag '**csv_to_snowflake**' in Airflow UI. Starts manually. Change to scheduled.
4. Check loaded data in Snowflake database using SQL command
   ```sql
   SELECT * FROM COMMITS.PUBLIC.COMMITS LIMIT 1000
   ```

## TO DO
### Step 3: Transform
- Use dbt to transform data and load into Snowflake.

---

### Step 4: Visualize
- Created visualizations in **Tableau**.
  ![Screenshot 2024-11-22 at 17 49 59](https://github.com/user-attachments/assets/20f51968-4be9-4069-8bc8-16aff042a867)

### Step 5: Make data accessible by API
calculated aggregated data 
query1 - Repo Weekly Commit Rate
	list of pairs: Repo commits count | Week 
```sql
 CREATE OR REPLACE TABLE COMMITS.PUBLIC.repo_commits_by_week (
  repo_id int NOT NULL,
  week DATE NOT NULL,
  repo_commits_count INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (repo_id)
);
```
Grant access to Snowflake account to fetch aggregated data.
```sql
GRANT INSERT, SELECT ON TABLE COMMITS.PUBLIC.repo_commits_by_week TO ROLE ETL_USER;
```
Insert sample data
```sql
INSERT INTO COMMITS.PUBLIC.repo_commits_by_week (repo_id, week, repo_commits_count)
VALUES
(101, '2025-09-01', 52),
(102, '2025-09-08', 35),
(101, '2025-09-08', 21);
```
---
## TO DO
### Step 6: Automate
- Automated data ingestion to upload only changes.

## Project Epics & Tasks Overview

| # | Epic| Key Tasks  | Priority |
|---|---|---|---|
| 1 | **Cost Management** | - Infrastructure cost<br>- Operational cost<br>- Development cost | High |
| 2 | **Project Management** | - Add tasks to projects on GitHub | High |
| 3 | **CI/CD and Infrastructure Setup** | - CI (Build in GitHub) - run tests<br>- CD<br>- Infra automation | High |
| 4 | **APIs and Proxy Layer** | - API to get data, to request data<br>- RL (API Proxy/Gateway)<br>&nbsp;&nbsp; - Caching<br>&nbsp;&nbsp; - Billing | High |
| 5 | **Build Data Pipeline** | - Add 2 fields: `lines_added`, `lines_deleted` from GitHub to Snowflake<br>- Create job to encode commits (job handler) in DAG<br>- Create DAG for users import to Snowflake to new fact table | High |
| 6 | **Schema and Joins Optimization** | - Consider using `author_id` instead of `username` for joins (P2) | Medium |
| 7 | **Code Quality and Testing** | - Define static types for each method<br>&nbsp;&nbsp; - Unit test + Function test<br>- Improve typing of input/output data using classes (P3)<br>- Refactor to remove duplicated code, introduce constants | Medium |
| 8 | **Documentation** | - Write spec about changes (`README.md`) | Medium |
| 9 | **Security and Observability** | - Security<br>- Logging / Monitoring / Alerting<br>&nbsp;&nbsp; - Runbook | High |
| 10 | **Data Management and Governance** | - Data Catalog<br>- Data Quality<br>- Data Source History<br>- Data Governance | Medium |
| 11 | **Data Processing and Scaling** | - Scale ETL pipeline to:<br>&nbsp;&nbsp; - More repos<br>&nbsp;&nbsp; - More orgs<br>&nbsp;&nbsp; - More users<br>&nbsp;&nbsp; - More commits<br>- Multi-tenancy | Low |

---

## Priority Legend:
- **High** — Must be done first for system to function
- **Medium** — Important but can be parallelized after foundations
- **Low** — Post-launch or scaling tasks

---

## TO DO
- Describe approach to security
- Set up CI/CD pipelines
- Configure scheduled incremental imports
- Implement monitoring and alerting
- Show current solution limitations using metrics
- Plan scalability to many repos, orgs, and users
- Ensure GDPR compliance
- Set up production infrastructure with automated configuration
- Estimate initial development and long-term support cost
- Improve dashboard: add commits metrics, show Snowflake DB schema
- Improve resiliency, ensure data consistency and optimize performance
- Add analysis of commits data using DeepSeek AI model

