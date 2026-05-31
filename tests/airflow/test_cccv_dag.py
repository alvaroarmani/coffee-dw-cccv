from pathlib import Path

from airflow.models import DagBag


def get_dag_bag() -> DagBag:
    dags_path = Path(__file__).resolve().parents[2] / "airflow" / "dags"
    return DagBag(dag_folder=str(dags_path), include_examples=False)


def test_cccv_dag_imports_without_errors():
    dag_bag = get_dag_bag()

    assert dag_bag.import_errors == {}


def test_cccv_dag_exists():
    dag_bag = get_dag_bag()

    dag = dag_bag.get_dag("cccv_coffee_prices_daily")

    assert dag is not None


def test_cccv_dag_has_expected_tasks():
    dag_bag = get_dag_bag()

    dag = dag_bag.get_dag("cccv_coffee_prices_daily")

    expected_tasks = {
        "start",
        "run_cccv_pipeline",
        "dbt_run",
        "dbt_test",
        "end",
    }

    assert set(dag.task_ids) == expected_tasks


def test_cccv_dag_task_dependencies():
    dag_bag = get_dag_bag()

    dag = dag_bag.get_dag("cccv_coffee_prices_daily")

    start = dag.get_task("start")
    run_pipeline = dag.get_task("run_cccv_pipeline")
    dbt_run = dag.get_task("dbt_run")
    dbt_test = dag.get_task("dbt_test")
    end = dag.get_task("end")

    assert run_pipeline.task_id in start.downstream_task_ids
    assert dbt_run.task_id in run_pipeline.downstream_task_ids
    assert dbt_test.task_id in dbt_run.downstream_task_ids
    assert end.task_id in dbt_test.downstream_task_ids
