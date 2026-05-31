.PHONY: help up down stop restart ps logs logs-postgres logs-pgadmin logs-airflow-webserver logs-airflow-scheduler build-airflow init-airflow pipeline test test-local test-airflow dbt-debug dbt-run dbt-test dbt-build dbt-docs-generate

help:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "Infraestrutura Docker:"
	@echo "  make up                         Sobe todos os containers"
	@echo "  make down                       Derruba os containers sem apagar volumes"
	@echo "  make stop                       Para os containers sem remover"
	@echo "  make restart                    Reinicia todos os containers"
	@echo "  make ps                         Lista containers do projeto"
	@echo ""
	@echo "Logs:"
	@echo "  make logs                       Mostra logs de todos os serviços"
	@echo "  make logs-postgres              Mostra logs do PostgreSQL do DW"
	@echo "  make logs-pgadmin               Mostra logs do pgAdmin"
	@echo "  make logs-airflow-webserver     Mostra logs do Airflow Webserver"
	@echo "  make logs-airflow-scheduler     Mostra logs do Airflow Scheduler"
	@echo ""
	@echo "Airflow:"
	@echo "  make build-airflow              Faz build da imagem customizada do Airflow"
	@echo "  make init-airflow               Inicializa banco interno e usuário do Airflow"
	@echo ""
	@echo "Pipeline:"
	@echo "  make pipeline                   Executa pipeline local CCCV"
	@echo ""
	@echo "dbt:"
	@echo "  make dbt-debug                  Testa conexão e configuração dbt"
	@echo "  make dbt-run                    Executa modelos dbt"
	@echo "  make dbt-test                   Executa testes dbt"
	@echo "  make dbt-build                  Executa dbt run + dbt test"
	@echo "  make dbt-docs-generate          Gera documentação dbt"
	@echo ""
	@echo "Testes:"
	@echo "  make test-local                 Roda testes locais sem Airflow"
	@echo "  make test-airflow               Roda testes da DAG dentro do container Airflow"
	@echo "  make test                       Roda testes locais e testes Airflow"

up:
	docker compose up -d

down:
	docker compose down

stop:
	docker compose stop

restart:
	docker compose down
	docker compose up -d

ps:
	docker compose ps

logs:
	docker compose logs

logs-postgres:
	docker compose logs postgres

logs-pgadmin:
	docker compose logs pgadmin

logs-airflow-webserver:
	docker compose logs airflow-webserver

logs-airflow-scheduler:
	docker compose logs airflow-scheduler

build-airflow:
	docker compose build airflow-init airflow-webserver airflow-scheduler

init-airflow:
	docker compose up airflow-init

pipeline:
	python -m src.run_cccv_pipeline

test-local:
	python -m pytest tests/extractors tests/loaders

test-airflow:
	docker compose exec airflow-scheduler python -m pytest /opt/airflow/project/tests/airflow/test_cccv_dag.py

test: test-local test-airflow

dbt-debug:
	dbt debug --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw

dbt-run:
	dbt run --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw

dbt-test:
	dbt test --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw

dbt-build:
	dbt run --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
	dbt test --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw

dbt-docs-generate:
	dbt docs generate --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
	