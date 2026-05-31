# Coffee DW CCCV

Projeto de Data Warehouse local para ingestão, tratamento e análise de cotações de café disponibilizadas pela CCCV.

O objetivo é construir uma POC de engenharia de dados com boas práticas de estruturação, versionamento, testes e documentação, simulando um fluxo próximo de um ambiente produtivo.

## Objetivo do projeto

Construir um pipeline local de dados para coletar cotações de café, armazenar os dados em PostgreSQL e transformá-los em camadas analíticas utilizando arquitetura Medallion.

O projeto será utilizado para estudar e demonstrar conceitos como:

- Ingestão de dados com Python
- Persistência em banco relacional
- Orquestração com Apache Airflow
- Transformação com dbt Core
- Modelagem em camadas Bronze, Silver e Gold
- Testes automatizados
- Versionamento com Git e GitHub
- Execução local com Docker

## Fonte de dados

A fonte principal do projeto é a página pública de cotações da CCCV:

```text
https://www.cccv.org.br/cotacao/
```

A página contém cotações de café por data, incluindo tipos como:

- Arábica bebida dura
- Arábica bebida rio
- Conilon

## Stack utilizada

- Python
- Docker
- Docker Compose
- PostgreSQL
- pgAdmin
- Apache Airflow
- dbt Core
- pytest
- Git
- GitHub Actions

## Arquitetura

O projeto seguirá a arquitetura Medallion:

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

Em fases futuras, o Airflow será responsável por orquestrar a execução do pipeline:

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

Nesta camada, o objetivo é preservar os dados próximos ao formato extraído, mantendo informações de rastreabilidade, como:

- Data da cotação
- Tipo do café
- Preço em reais
- URL de origem
- Data e hora de extração
- Data e hora de carga

### Silver

Camada de dados limpos, padronizados e preparados para análise.

Nesta etapa serão aplicadas regras como:

- Padronização de nomes de colunas
- Conversão de tipos
- Tratamento de valores nulos
- Remoção de duplicidades
- Validações básicas de qualidade

### Gold

Camada final de dados analíticos.

Nesta camada serão criados modelos voltados para análise de negócio, como:

- Evolução diária do preço do Conilon
- Resumo mensal de preços
- Comparação entre tipos de café
- Indicadores de variação e tendência

## Estrutura do projeto

```text
coffee-dw-cccv/
│
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── plugins/
│
├── dbt/
│   └── coffee_dw/
│       ├── models/
│       │   ├── bronze/
│       │   ├── silver/
│       │   └── gold/
│       ├── seeds/
│       ├── snapshots/
│       └── tests/
│
├── docker/
│   ├── airflow/
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
├── README.md
└── requirements.txt
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

O arquivo `.env.example` contém as variáveis necessárias para o ambiente local, como usuário, senha e nome do banco PostgreSQL.

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

# Source
CCCV_COTACAO_URL=https://www.cccv.org.br/cotacao/
```

## Infraestrutura local

Nesta etapa do projeto, os seguintes serviços são executados via Docker Compose:

- PostgreSQL
- pgAdmin

Futuramente serão adicionados:

- Apache Airflow
- dbt Core
- execução orquestrada do pipeline

## Como subir a infraestrutura local

Subir PostgreSQL e pgAdmin:

```bash
docker compose up -d
```

Verificar se os containers estão rodando:

```bash
docker compose ps
```

Acessar o pgAdmin no navegador:

```text
http://localhost:5050
```

Credenciais padrão do pgAdmin:

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
- Fora do Docker, o Python acessa o PostgreSQL usando `127.0.0.1:5433`.

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

Esses schemas são criados automaticamente na primeira inicialização do PostgreSQL por meio do script:

```text
docker/postgres/init/01_create_schemas.sql
```

## Tabela Bronze

A primeira tabela criada no projeto é:

```text
bronze.raw_cccv_daily_prices
```

Ela armazena os dados extraídos da CCCV.

Campos principais:

```text
id
price_date
coffee_type
coffee_description
price_brl
source_url
extracted_at
loaded_at
```

A tabela possui uma restrição de unicidade para evitar duplicidade no carregamento:

```text
price_date + coffee_type + source_url
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

O extractor atualmente captura os seguintes campos:

```text
price_date
coffee_type
coffee_description
price_brl
source_url
extracted_at
```

Exemplo de registro estruturado:

```text
{
  "price_date": "2026-03-02",
  "coffee_type": "conilon",
  "coffee_description": "Conilon",
  "price_brl": "984.00",
  "source_url": "https://www.cccv.org.br/cotacao/",
  "extracted_at": "2026-05-30T..."
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
SELECT coffee_type, COUNT(*) AS total
FROM bronze.raw_cccv_daily_prices
GROUP BY coffee_type
ORDER BY coffee_type;
```

Exemplo de resultado esperado:

```text
arabica_dura | 10
arabica_rio  | 10
conilon      | 10
```

Consultar registros carregados:

```sql
SELECT *
FROM bronze.raw_cccv_daily_prices
ORDER BY price_date, coffee_type
LIMIT 30;
```

## Testes

O projeto utiliza `pytest` para testes automatizados.

Rodar todos os testes:

```bash
python -m pytest
```

Atualmente os testes cobrem:

- Conversão de valores monetários no padrão brasileiro
- Extração de mês e ano da cotação
- Parse de HTML de exemplo da CCCV
- Geração de registros estruturados por tipo de café
- Conversão de valores `Decimal` antes da carga no banco

## Comandos úteis

Subir containers:

```bash
docker compose up -d
```

Parar containers sem remover:

```bash
docker compose stop
```

Derrubar containers:

```bash
docker compose down
```

Derrubar containers e volumes:

```bash
docker compose down -v
```

Atenção: o comando acima remove os volumes Docker e apaga os dados locais do PostgreSQL.

Ver logs:

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

Ver containers ativos:

```bash
docker compose ps
```

Testar conexão com PostgreSQL pelo container:

```bash
docker exec -it coffee_dw_postgres psql -U coffee_user -d coffee_dw -c "SELECT 1;"
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

- Criação da DAG de ingestão
- Orquestração do extractor e loader
- Testes básicos da DAG

### Fase 6 — dbt

- Criação do projeto dbt
- Modelos Silver
- Modelos Gold
- Testes e documentação dbt

### Fase 7 — GitHub Actions

- Pipeline de CI
- Execução automática de testes
- Validação do projeto em pull requests

## Status atual

Fase atual:

Fase 4 — Loader PostgreSQL
