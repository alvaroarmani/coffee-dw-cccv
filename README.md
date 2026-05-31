# Coffee DW CCCV

Projeto de Data Warehouse local para ingestão, tratamento, orquestração e análise de cotações de café disponibilizadas pela CCCV.

O objetivo é construir uma POC de engenharia de dados com boas práticas de estruturação, versionamento, testes e documentação, simulando um fluxo próximo de um ambiente produtivo.

## Objetivo do projeto

Construir um pipeline local de dados para coletar cotações de café, armazenar os dados em PostgreSQL, orquestrar a execução com Apache Airflow e transformar os dados em camadas analíticas utilizando dbt Core e arquitetura Medallion.

O projeto será utilizado para estudar e demonstrar conceitos como:

- Ingestão de dados com Python
- Persistência em banco relacional
- Orquestração com Apache Airflow
- Transformação com dbt Core
- Modelagem em camadas Bronze, Silver e Gold
- Testes automatizados
- Versionamento com Git e GitHub
- Execução local com Docker
- Boas práticas de organização de projeto de dados

## Fonte de dados

A fonte principal do projeto é a página pública de cotações da CCCV:

```text
https://www.cccv.org.br/cotacao/
```

A página contém cotações de café por data, tipo de café e safra.

Tipos de café atualmente tratados:

- Arábica bebida dura
- Arábica bebida rio
- Conilon

A estrutura da tabela de origem possui colunas por safra. Por isso, o projeto considera a safra como um atributo analítico importante.

Exemplo de safras tratadas:

```text
2025/2026
2026/2027
```

## Stack utilizada

- Python
- Docker
- Docker Compose
- PostgreSQL
- pgAdmin
- Apache Airflow
- dbt Core
- dbt-postgres
- pytest
- Git
- GitHub Actions

## Arquitetura

O projeto segue a arquitetura Medallion:

```text
Fonte CCCV
    ↓
Python Extractor
    ↓
Python Loader
    ↓
PostgreSQL - Bronze
    ↓
dbt - Silver
    ↓
dbt - Gold
    ↓
Camada analítica
```

Com orquestração via Airflow:

```text
Airflow DAG
    ↓
Extractor CCCV
    ↓
Loader PostgreSQL
    ↓
dbt run
    ↓
dbt test
```

## Camadas do Data Warehouse

### Bronze

Camada de dados brutos ou semitratados vindos da fonte.

Nesta camada, o objetivo é preservar os dados próximos ao formato extraído, mantendo informações de rastreabilidade.

Principais campos:

```text
id
price_date
coffee_type
coffee_description
harvest_year
price_brl
source_url
extracted_at
loaded_at
```

### Silver

Camada de dados limpos, padronizados e preparados para análise.

Nesta etapa são aplicadas regras como:

- Padronização de nomes de colunas
- Conversão de tipos
- Validação de campos obrigatórios
- Validação de valores aceitos
- Organização por tipo de café e safra

### Gold

Camada final de dados analíticos.

Nesta camada são criados modelos voltados para análise de negócio, como:

- Evolução diária do preço do Conilon por safra
- Resumo mensal de preços por tipo de café e safra
- Comparação entre safras
- Análise de diferença de preço entre safra atual e safra futura

## Estrutura do projeto

```text
coffee-dw-cccv/
│
├── airflow/
│   ├── dags/
│   │   └── cccv_coffee_prices_dag.py
│   ├── logs/
│   ├── plugins/
│   └── config/
│
├── dbt/
│   └── coffee_dw/
│       ├── macros/
│       │   └── generate_schema_name.sql
│       ├── models/
│       │   ├── bronze/
│       │   │   └── _sources.yml
│       │   ├── silver/
│       │   │   ├── stg_cccv_coffee_prices.sql
│       │   │   └── _silver.yml
│       │   └── gold/
│       │       ├── mart_conilon_daily_prices.sql
│       │       ├── mart_coffee_monthly_summary.sql
│       │       ├── mart_harvest_comparison.sql
│       │       └── _gold.yml
│       ├── seeds/
│       ├── snapshots/
│       ├── tests/
│       ├── dbt_project.yml
│       └── profiles.yml
│
├── docker/
│   ├── airflow/
│   │   └── Dockerfile
│   ├── dbt/
│   └── postgres/
│       └── init/
│           ├── 01_create_schemas.sql
│           └── 02_create_bronze_tables.sql
│
├── src/
│   ├── extractors/
│   │   └── cccv_extractor.py
│   ├── loaders/
│   │   └── postgres_loader.py
│   ├── utils/
│   └── run_cccv_pipeline.py
│
├── tests/
│   ├── airflow/
│   │   └── test_cccv_dag.py
│   ├── extractors/
│   │   └── test_cccv_extractor.py
│   └── loaders/
│       └── test_postgres_loader.py
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── pytest.ini
├── README.md
├── requirements.txt
└── requirements-airflow.txt
```

## Pré-requisitos

Antes de executar o projeto localmente, é necessário ter instalado:

- Git
- Python 3.11 ou superior
- Docker Desktop
- Docker Compose

## Configuração do ambiente

Crie o arquivo `.env` a partir do exemplo:

```bash
copy .env.example .env
```

O arquivo `.env.example` contém as variáveis necessárias para o ambiente local, como usuário, senha, nome do banco PostgreSQL, configurações do pgAdmin e configurações do Airflow.

O arquivo `.env` não deve ser versionado no Git.

Exemplo de configuração local esperada:

```env
# Project
PROJECT_NAME=coffee-dw-cccv

# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_LOCAL_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=coffee_dw
POSTGRES_USER=coffee_user
POSTGRES_PASSWORD=coffee_password

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin

# Airflow
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=./airflow
AIRFLOW_IMAGE_NAME=coffee-dw-airflow:latest
AIRFLOW_ADMIN_USERNAME=airflow
AIRFLOW_ADMIN_PASSWORD=airflow
AIRFLOW_ADMIN_FIRSTNAME=Airflow
AIRFLOW_ADMIN_LASTNAME=Admin
AIRFLOW_ADMIN_EMAIL=airflow@example.com

# Source
CCCV_COTACAO_URL=https://www.cccv.org.br/cotacao/
```

## Infraestrutura local

Os seguintes serviços são executados via Docker Compose:

```text
postgres
pgadmin
airflow-db
airflow-init
airflow-webserver
airflow-scheduler
```

Descrição dos serviços:

```text
postgres              Banco PostgreSQL do Data Warehouse
pgadmin               Interface web para acessar o PostgreSQL
airflow-db            Banco interno de metadados do Airflow
airflow-init          Serviço de inicialização do Airflow
airflow-webserver     Interface web do Airflow
airflow-scheduler     Scheduler do Airflow
```

## Como subir a infraestrutura local

Subir todos os containers:

```bash
docker compose up -d
```

Verificar se os containers estão rodando:

```bash
docker compose ps
```

Parar containers sem remover:

```bash
docker compose stop
```

Derrubar containers sem apagar volumes:

```bash
docker compose down
```

Derrubar containers e apagar volumes:

```bash
docker compose down -v
```

Atenção: o comando `docker compose down -v` remove os volumes Docker e apaga os dados locais do PostgreSQL.

## Acessar pgAdmin

Acesse no navegador:

```text
http://localhost:5050
```

Credenciais padrão:

```text
Email: admin@admin.com
Senha: admin
```

Configuração do servidor PostgreSQL dentro do pgAdmin:

```text
Host: postgres
Port: 5432
Database: coffee_dw
User: coffee_user
Password: coffee_password
```

Observação importante:

- Dentro do Docker, o pgAdmin acessa o PostgreSQL usando `postgres:5432`.
- Fora do Docker, no Windows, o Python e o dbt acessam o PostgreSQL usando `127.0.0.1:5433`.

## Banco de dados

O banco principal do projeto é:

```text
coffee_dw
```

Ele possui três schemas principais:

```text
bronze
silver
gold
```

Esses schemas são criados pelo script:

```text
docker/postgres/init/01_create_schemas.sql
```

## Tabela Bronze

A tabela Bronze principal é:

```text
bronze.raw_cccv_daily_prices
```

Ela armazena os dados extraídos da CCCV.

Campos:

```text
id
price_date
coffee_type
coffee_description
harvest_year
price_brl
source_url
extracted_at
loaded_at
```

A tabela possui uma restrição de unicidade para evitar duplicidade no carregamento:

```text
price_date + coffee_type + harvest_year + source_url
```

Script responsável pela criação da tabela:

```text
docker/postgres/init/02_create_bronze_tables.sql
```

## Extractor da CCCV

O projeto possui um extractor Python responsável por acessar a página de cotação da CCCV e transformar os dados em registros estruturados.

Arquivo principal:

```text
src/extractors/cccv_extractor.py
```

Rodar o extractor localmente:

```bash
python -m src.extractors.cccv_extractor
```

O extractor captura os seguintes campos:

```text
price_date
coffee_type
coffee_description
harvest_year
price_brl
source_url
extracted_at
```

A página da CCCV possui uma tabela com seis colunas de preço, considerando tipo de café e safra:

```text
1. Arábica bebida dura - safra 2025/2026
2. Arábica bebida rio  - safra 2025/2026
3. Arábica bebida dura - safra 2026/2027
4. Arábica bebida rio  - safra 2026/2027
5. Conilon             - safra 2025/2026
6. Conilon             - safra 2026/2027
```

Valores ausentes, representados por `-`, são ignorados pelo parser.

Exemplo de registro estruturado:

```text
{
  "price_date": "2026-05-04",
  "coffee_type": "conilon",
  "coffee_description": "Conilon bica corrida, tipo 7/8",
  "harvest_year": "2025/2026",
  "price_brl": "873.00",
  "source_url": "https://www.cccv.org.br/cotacao/",
  "extracted_at": "2026-05-31T..."
}
```

## Loader PostgreSQL

O projeto possui um loader Python responsável por carregar os registros extraídos para a camada Bronze do PostgreSQL.

Arquivo principal:

```text
src/loaders/postgres_loader.py
```

Tabela de destino:

```text
bronze.raw_cccv_daily_prices
```

O loader utiliza `ON CONFLICT` para evitar duplicidade. Caso o mesmo registro já exista, ele é atualizado.

A chave lógica utilizada no conflito é:

```text
price_date
coffee_type
harvest_year
source_url
```

## Executar pipeline local

Executar extração e carga no PostgreSQL:

```bash
python -m src.run_cccv_pipeline
```

Resultado esperado:

```text
Iniciando pipeline CCCV...
Registros extraídos: 30
Conectando ao PostgreSQL em: postgresql+pg8000://coffee_user:coffee_password@127.0.0.1:5433/coffee_dw
Registros carregados/atualizados: 30
Pipeline finalizado com sucesso.
```

A quantidade de registros pode variar conforme a cotação disponível na página da CCCV.

## Validar dados no PostgreSQL

No pgAdmin, execute:

```sql
SELECT
    coffee_type,
    harvest_year,
    COUNT(*) AS total
FROM bronze.raw_cccv_daily_prices
GROUP BY
    coffee_type,
    harvest_year
ORDER BY
    coffee_type,
    harvest_year;
```

Consultar registros carregados:

```sql
SELECT
    price_date,
    coffee_type,
    coffee_description,
    harvest_year,
    price_brl
FROM bronze.raw_cccv_daily_prices
ORDER BY
    price_date,
    coffee_type,
    harvest_year;
```

Validar dados de Conilon:

```sql
SELECT
    price_date,
    coffee_type,
    harvest_year,
    price_brl
FROM bronze.raw_cccv_daily_prices
WHERE coffee_type = 'conilon'
ORDER BY
    price_date,
    harvest_year;
```

## Airflow

O projeto utiliza Apache Airflow para orquestrar o pipeline de ingestão.

Acessar a interface web do Airflow:

```text
http://localhost:8080
```

Credenciais padrão:

```text
Usuário: airflow
Senha: airflow
```

DAG principal:

```text
cccv_coffee_prices_daily
```

Arquivo da DAG:

```text
airflow/dags/cccv_coffee_prices_dag.py
```

A DAG executa o seguinte fluxo:

```text
start
  ↓
run_cccv_pipeline
  ↓
end
```

A task `run_cccv_pipeline` executa o pipeline Python responsável por:

```text
1. Extrair as cotações da CCCV
2. Transformar os dados em registros estruturados
3. Carregar os dados na tabela bronze.raw_cccv_daily_prices
```

Dentro do Airflow, o PostgreSQL do Data Warehouse é acessado por:

```text
Host: postgres
Port: 5432
```

Fora do Docker, no Windows, o PostgreSQL é acessado por:

```text
Host: 127.0.0.1
Port: 5433
```

## dbt

O projeto utiliza dbt Core para transformar os dados da camada Bronze em modelos Silver e Gold.

Projeto dbt:

```text
dbt/coffee_dw
```

O dbt se conecta ao PostgreSQL local usando o arquivo:

```text
dbt/coffee_dw/profiles.yml
```

Como o dbt roda localmente no Windows, a conexão usa:

```text
Host: 127.0.0.1
Port: 5433
Database: coffee_dw
```

## Modelos dbt

### Source Bronze

Fonte configurada no dbt:

```text
bronze.raw_cccv_daily_prices
```

Arquivo:

```text
dbt/coffee_dw/models/bronze/_sources.yml
```

### Silver

Modelo Silver:

```text
silver.stg_cccv_coffee_prices
```

Arquivo:

```text
dbt/coffee_dw/models/silver/stg_cccv_coffee_prices.sql
```

Esse modelo padroniza os dados da Bronze e mantém os principais campos analíticos:

```text
raw_price_id
price_date
coffee_type
coffee_description
harvest_year
price_brl
source_url
extracted_at
loaded_at
```

### Gold

Modelos Gold:

```text
gold.mart_conilon_daily_prices
gold.mart_coffee_monthly_summary
gold.mart_harvest_comparison
```

#### `mart_conilon_daily_prices`

Permite analisar a evolução diária do café Conilon por safra.

Campos principais:

```text
price_date
coffee_type
coffee_description
harvest_year
price_brl
source_url
extracted_at
loaded_at
```

#### `mart_coffee_monthly_summary`

Cria um resumo mensal por tipo de café e safra.

Campos principais:

```text
reference_month
coffee_type
coffee_description
harvest_year
total_quotes
min_price_brl
max_price_brl
avg_price_brl
```

#### `mart_harvest_comparison`

Compara preços entre as safras `2025/2026` e `2026/2027`.

Campos principais:

```text
price_date
coffee_type
coffee_description
price_2025_2026
price_2026_2027
price_diff_brl
price_diff_pct
```

Esse modelo permite responder perguntas como:

- A safra nova está sendo cotada acima ou abaixo da safra atual?
- Qual tipo de café tem maior diferença entre safras?
- Quando a safra futura começou a ter preço?
- Existe diferença relevante entre Conilon e Arábica por safra?

## Comandos dbt

Validar configuração e conexão:

```bash
dbt debug --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
```

Executar modelos:

```bash
dbt run --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
```

Executar testes:

```bash
dbt test --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
```

Executar run + test:

```bash
dbt run --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
dbt test --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
```

Gerar documentação dbt:

```bash
dbt docs generate --project-dir dbt/coffee_dw --profiles-dir dbt/coffee_dw
```

## Validações analíticas no PostgreSQL

Consultar dados Silver:

```sql
SELECT
    price_date,
    coffee_type,
    harvest_year,
    price_brl
FROM silver.stg_cccv_coffee_prices
ORDER BY
    price_date,
    coffee_type,
    harvest_year
LIMIT 30;
```

Consultar preços diários do Conilon:

```sql
SELECT
    price_date,
    harvest_year,
    price_brl
FROM gold.mart_conilon_daily_prices
ORDER BY
    price_date,
    harvest_year;
```

Consultar resumo mensal:

```sql
SELECT *
FROM gold.mart_coffee_monthly_summary
ORDER BY
    reference_month,
    coffee_type,
    harvest_year;
```

Consultar comparação entre safras:

```sql
SELECT *
FROM gold.mart_harvest_comparison
ORDER BY
    price_date,
    coffee_type;
```

## Testes

O projeto utiliza `pytest` para testes automatizados.

Existem dois grupos de testes:

- Testes locais, que rodam no `.venv` do projeto
- Testes do Airflow, que rodam dentro do container do Airflow

Rodar testes locais:

```bash
python -m pytest tests/extractors tests/loaders
```

Rodar testes da DAG dentro do container do Airflow:

```bash
docker compose exec airflow-scheduler python -m pytest /opt/airflow/project/tests/airflow/test_cccv_dag.py
```

Atualmente os testes cobrem:

- Conversão de valores monetários no padrão brasileiro
- Extração de mês e ano da cotação
- Parse de HTML de exemplo da CCCV
- Geração de registros estruturados por tipo de café e safra
- Conversão de valores `Decimal` antes da carga no banco
- Importação da DAG do Airflow
- Estrutura básica da DAG
- Dependências entre tasks da DAG

## Comandos úteis

O projeto possui um `Makefile` para padronizar comandos.

Listar comandos disponíveis:

```bash
make help
```

Subir containers:

```bash
make up
```

Parar containers:

```bash
make stop
```

Derrubar containers:

```bash
make down
```

Ver containers ativos:

```bash
make ps
```

Executar pipeline local:

```bash
make pipeline
```

Rodar testes locais:

```bash
make test-local
```

Rodar testes da DAG:

```bash
make test-airflow
```

Rodar dbt debug:

```bash
make dbt-debug
```

Rodar dbt run:

```bash
make dbt-run
```

Rodar dbt test:

```bash
make dbt-test
```

Rodar dbt run + test:

```bash
make dbt-build
```

## Comandos Docker úteis

Ver logs de todos os serviços:

```bash
docker compose logs
```

Ver logs do PostgreSQL:

```bash
docker compose logs postgres
```

Ver logs do pgAdmin:

```bash
docker compose logs pgadmin
```

Ver logs do Airflow Webserver:

```bash
docker compose logs airflow-webserver
```

Ver logs do Airflow Scheduler:

```bash
docker compose logs airflow-scheduler
```

Testar conexão com PostgreSQL pelo container:

```bash
docker exec -it coffee_dw_postgres psql -U coffee_user -d coffee_dw -c "SELECT 1;"
```

## Troubleshooting

### Airflow Webserver reiniciando

Verifique os logs:

```bash
docker compose logs --tail=100 airflow-webserver
```

### Airflow não reconhece a DAG

Verifique os logs do scheduler:

```bash
docker compose logs --tail=100 airflow-scheduler
```

### PostgreSQL local não conecta no Python

Confirme se a porta local está acessível:

```powershell
Test-NetConnection 127.0.0.1 -Port 5433
```

### Erro de senha no PostgreSQL

Resetar senha do usuário local:

```bash
docker exec -it coffee_dw_postgres psql -U coffee_user -d coffee_dw -c "ALTER USER coffee_user WITH PASSWORD 'coffee_password';"
```

### dbt criou schemas com nomes compostos

O projeto usa a macro:

```text
dbt/coffee_dw/macros/generate_schema_name.sql
```

Ela força o dbt a criar os modelos exatamente nos schemas:

```text
silver
gold
```

em vez de schemas como:

```text
silver_silver
silver_gold
```

## Roadmap

### Fase 1 — Estrutura inicial

- Criação da estrutura de pastas
- Inicialização do Git
- Criação dos arquivos base
- Primeiro commit do projeto

### Fase 2 — Infraestrutura local

- Configuração do Docker Compose
- Subida do PostgreSQL
- Subida do pgAdmin
- Criação dos schemas Bronze, Silver e Gold

### Fase 3 — Extractor da CCCV

- Criação do extractor Python
- Coleta da página de cotação da CCCV
- Parse dos dados de cotação
- Testes unitários do extractor

### Fase 4 — Loader PostgreSQL

- Criação da tabela Bronze
- Criação do loader Python
- Carga dos dados extraídos no PostgreSQL
- Testes básicos do loader

### Fase 5 — Airflow

- Criação da imagem customizada do Airflow
- Subida do Airflow via Docker Compose
- Criação da DAG de ingestão
- Orquestração do extractor e loader
- Testes básicos da DAG

### Fase 6 — dbt

- Criação do projeto dbt
- Configuração de source Bronze
- Criação do modelo Silver
- Criação dos modelos Gold
- Criação de testes dbt
- Validação dos modelos no PostgreSQL

### Fase 7 — GitHub Actions

- Criação do repositório remoto
- Push do projeto para o GitHub
- Criação de pipeline de CI
- Execução automática de testes
- Validação do projeto em pull requests

### Fase 8 — Documentação final e portfólio

- Revisão final do README
- Documentação de decisões técnicas
- Documentação de arquitetura
- Exemplos de queries analíticas
- Preparação do projeto para portfólio

## Status atual

Fase atual:

```text
Fase 6 — dbt
```
