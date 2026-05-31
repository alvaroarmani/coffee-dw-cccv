from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from src.run_cccv_pipeline import main as run_cccv_pipeline

default_args = {
    "owner": "airflow",
    "retries": 1,
}


DBT_PROJECT_DIR = "/opt/airflow/project/dbt/coffee_dw"
DBT_PROFILES_DIR = "/opt/airflow/project/dbt/coffee_dw"


with DAG(
    dag_id="cccv_coffee_prices_daily",
    description="Pipeline diário para extrair cotações de café da CCCV, carregar Bronze e atualizar modelos dbt.",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["coffee", "cccv", "bronze", "dbt", "datawarehouse"],
) as dag:

    start = EmptyOperator(
        task_id="start",
    )

    run_pipeline = PythonOperator(
        task_id="run_cccv_pipeline",
        python_callable=run_cccv_pipeline,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            f"dbt run "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR} "
            f"--target airflow"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"dbt test "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROFILES_DIR} "
            f"--target airflow"
        ),
    )

    end = EmptyOperator(
        task_id="end",
    )

    start >> run_pipeline >> dbt_run >> dbt_test >> end
