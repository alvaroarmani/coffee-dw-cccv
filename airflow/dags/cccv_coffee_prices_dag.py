from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from src.run_cccv_pipeline import main as run_cccv_pipeline

default_args = {
    "owner": "airflow",
    "retries": 1,
}


with DAG(
    dag_id="cccv_coffee_prices_daily",
    description="Pipeline diário para extrair cotações de café da CCCV e carregar na camada Bronze.",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["coffee", "cccv", "bronze", "datawarehouse"],
) as dag:

    start = EmptyOperator(
        task_id="start",
    )

    run_pipeline = PythonOperator(
        task_id="run_cccv_pipeline",
        python_callable=run_cccv_pipeline,
    )

    end = EmptyOperator(
        task_id="end",
    )

    start >> run_pipeline >> end
