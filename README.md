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

## Status

Fase atual: estrutura inicial do projeto.
