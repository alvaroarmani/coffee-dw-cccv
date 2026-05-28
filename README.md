# Coffee DW CCCV

Projeto de Data Warehouse local para ingestão, tratamento e análise de cotações de café da CCCV.

## Objetivo

Construir uma POC de engenharia de dados utilizando:

- Docker
- PostgreSQL
- Apache Airflow
- dbt Core
- Python
- GitHub Actions

## Fonte de dados

Fonte principal:

https://www.cccv.org.br/cotacao/

## Arquitetura

O projeto seguirá a arquitetura Medallion:

```text
Fonte CCCV
    ↓
Airflow
    ↓
PostgreSQL - Bronze
    ↓
dbt - Silver
    ↓
dbt - Gold
```

## Camadas

### Bronze

Dados brutos ou semitratados vindos da fonte.

### Silver

Dados limpos, padronizados e preparados para análise.

### Gold

Tabelas finais de negócio e indicadores analíticos.

## Infraestrutura local

Nesta fase, o projeto sobe os seguintes serviços via Docker Compose:

- PostgreSQL
- pgAdmin

## Como subir a infraestrutura local

Pré-requisitos:

- Docker Desktop instalado
- Docker Compose disponível

Criar o arquivo `.env` a partir do exemplo:

```bash
copy .env.example .env
```

Subir PostgreSQL e pgAdmin:

```bash
docker compose up -d
```

Verificar containers:

```bash
docker compose ps
```

Acessar pgAdmin no navegador:

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

## Schemas do banco

O banco `coffee_dw` possui três schemas principais:

```text
bronze
silver
gold
```

## Comandos úteis

Subir containers:

```bash
docker compose up -d
```

Parar containers:

```bash
docker compose stop
```

Derrubar containers:

```bash
docker compose down
```

Ver logs:

```bash
docker compose logs
```

Ver containers ativos:

```bash
docker compose ps
```

## Status

Fase atual: Docker Compose com PostgreSQL e pgAdmin.
