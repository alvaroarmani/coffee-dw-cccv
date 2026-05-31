# Guia de execução local

Este documento descreve como executar o projeto Coffee DW CCCV do zero.

## Pré-requisitos

- Git
- Python 3.11+
- Docker Desktop
- Docker Compose

## Clonar o repositório

```bash
git clone https://github.com/alvaroarmani/coffee-dw-cccv.git
cd coffee-dw-cccv
```

## Criar ambiente virtual

```bash
python -m venv .venv
```

Ativar no PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Criar arquivo de ambiente

```bash
copy .env.example .env
```

## Subir infraestrutura

```bash
docker compose up -d
```

## Acessar pgAdmin

```text
http://localhost:5050
```

Credenciais:

```text
Email: admin@admin.com
Senha: admin
```

## Acessar Airflow

```text
http://localhost:8080
```

Credenciais:

```text
Usuário: airflow
Senha: airflow
```

## Executar pipeline local

```bash
python -m src.run_cccv_pipeline
```

## Executar dbt

```bash
dbt debug --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
dbt run --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
dbt test --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
```

## Rodar testes

Testes locais:

```bash
python -m pytest tests/extractors tests/loaders
```

Teste da DAG:

```bash
docker compose exec airflow-scheduler python -m pytest /opt/airflow/project/tests/airflow/test_cccv_dag.py
```
