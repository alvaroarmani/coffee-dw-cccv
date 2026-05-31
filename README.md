# Coffee DW CCCV

Projeto de Data Warehouse local para ingestão, tratamento e análise de cotações de café disponibilizadas pela CCCV.

O objetivo é construir uma POC de engenharia de dados com boas práticas de estruturação, versionamento, testes e documentação, simulando um fluxo próximo de um ambiente produtivo.

## Objetivo do projeto

Construir um pipeline local de dados para coletar cotações de café, armazenar os dados em PostgreSQL e transformá-los em camadas analíticas utilizando arquitetura Medallion.

O projeto será utilizado para estudar e demonstrar conceitos como:

- ingestão de dados com Python;
- persistência em banco relacional;
- orquestração com Apache Airflow;
- transformação com dbt Core;
- modelagem em camadas Bronze, Silver e Gold;
- testes automatizados;
- versionamento com Git e GitHub;
- execução local com Docker.

## Fonte de dados

A fonte principal do projeto é a página pública de cotações da CCCV:

```text
https://www.cccv.org.br/cotacao/
```

A página contém cotações de café por data, incluindo tipos como:

- Arábica bebida dura;
- Arábica bebida rio;
- Conilon.

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
Airflow
    ↓
PostgreSQL - Bronze
    ↓
dbt - Silver
    ↓
dbt - Gold
```

## Camadas do Data Warehouse

### Bronze

Camada de dados brutos ou semitratados vindos da fonte.

Nesta camada, o objetivo é preservar os dados próximos ao formato original, mantendo informações de rastreabilidade, como fonte, data de extração e data da cotação.

### Silver

Camada de dados limpos, padronizados e preparados para análise.

Nesta etapa serão aplicadas regras como:

- padronização de nomes de colunas;
- conversão de tipos;
- tratamento de valores nulos;
- remoção de duplicidades;
- validações básicas de qualidade.

### Gold

Camada final de dados analíticos.

Nesta camada serão criados modelos voltados para análise de negócio, como:

- evolução diária do preço do Conilon;
- resumo mensal de preços;
- comparação entre tipos de café;
- indicadores de variação e tendência.

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
│
├── src/
│   ├── extractors/
│   ├── loaders/
│   └── utils/
│
├── tests/
│   ├── airflow/
│   ├── extractors/
│   └── loaders/
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

## Infraestrutura local

Nesta etapa do projeto, os seguintes serviços são executados via Docker Compose:

- PostgreSQL;
- pgAdmin.

Futuramente serão adicionados:

- Apache Airflow;
- dbt Core;
- execução orquestrada do pipeline.

## Pré-requisitos

Antes de executar o projeto localmente, é necessário ter instalado:

- Git;
- Python 3.11 ou superior;
- Docker Desktop;
- Docker Compose.

## Configuração do ambiente

Crie o arquivo `.env` a partir do exemplo:

```bash
copy .env.example .env
```

O arquivo `.env.example` contém as variáveis necessárias para o ambiente local, como usuário, senha e nome do banco PostgreSQL.

O arquivo `.env` não deve ser versionado no Git.

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

## Extractor da CCCV

O projeto possui um extractor Python responsável por acessar a página de cotação da CCCV e transformar os dados em registros estruturados.

Arquivo principal:

```text
src/extractors/cccv_extractor.py
```

Rodar o extractor localmente:

```bash
python src/extractors/cccv_extractor.py
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

Exemplo de saída esperada:

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

## Testes

O projeto utiliza `pytest` para testes automatizados.

Rodar todos os testes:

```bash
python -m pytest
```

Atualmente os testes cobrem:

- conversão de valores monetários no padrão brasileiro;
- extração de mês e ano da cotação;
- parse de HTML de exemplo da CCCV;
- geração de registros estruturados por tipo de café.

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

> Atenção: o comando acima remove os volumes Docker e apaga os dados locais do PostgreSQL.

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

## Roadmap

### Fase 1 — Estrutura inicial

- Criação da estrutura de pastas;
- Inicialização do Git;
- Criação dos arquivos base;
- Primeiro commit do projeto.

### Fase 2 — Infraestrutura local

- Configuração do Docker Compose;
- Subida do PostgreSQL;
- Subida do pgAdmin;
- Criação dos schemas Bronze, Silver e Gold.

### Fase 3 — Extractor da CCCV

- Criação do extractor Python;
- Coleta da página de cotação da CCCV;
- Parse dos dados de cotação;
- Testes unitários do extractor.

### Fase 4 — Loader PostgreSQL

- Criação da tabela Bronze;
- Criação do loader Python;
- Carga dos dados extraídos no PostgreSQL.

### Fase 5 — Airflow

- Criação da DAG de ingestão;
- Orquestração do extractor e loader;
- Testes básicos da DAG.

### Fase 6 — dbt

- Criação do projeto dbt;
- Modelos Silver;
- Modelos Gold;
- Testes e documentação dbt.

### Fase 7 — GitHub Actions

- Pipeline de CI;
- Execução automática de testes;
- Validação do projeto em pull requests.

## Status atual

Fase atual:

Fase 3 — Extractor da CCCV
