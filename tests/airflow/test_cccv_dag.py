from pathlib import Path

from airflow.models import DagBag


def test_cccv_dag_imports_without_errors():
    dags_path = Path(__file__).resolve().parents[2] / "airflow" / "dags"

    dag_bag = DagBag(dag_folder=str(dags_path), include_examples=False)

    assert dag_bag.import_errors == {}


def test_cccv_dag_exists():
    dags_path = Path(__file__).resolve().parents[2] / "airflow" / "dags"

    dag_bag = DagBag(dag_folder=str(dags_path), include_examples=False)

    dag = dag_bag.get_dag("cccv_coffee_prices_daily")

    assert dag is not None


def test_cccv_dag_has_expected_tasks():
    dags_path = Path(__file__).resolve().parents[2] / "airflow" / "dags"

    dag_bag = DagBag(dag_folder=str(dags_path), include_examples=False)

    dag = dag_bag.get_dag("cccv_coffee_prices_daily")

    expected_tasks = {
        "start",
        "run_cccv_pipeline",
        "end",
    }

    assert set(dag.task_ids) == expected_tasks


def test_cccv_dag_task_dependencies():
    dags_path = Path(__file__).resolve().parents[2] / "airflow" / "dags"

    dag_bag = DagBag(dag_folder=str(dags_path), include_examples=False)

    dag = dag_bag.get_dag("cccv_coffee_prices_daily")

    start = dag.get_task("start")
    run_pipeline = dag.get_task("run_cccv_pipeline")
    end = dag.get_task("end")

    assert run_pipeline.task_id in start.downstream_task_ids
    assert end.task_id in run_pipeline.downstream_task_ids
