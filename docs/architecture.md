# Arquitetura do projeto

## Visão geral

O projeto Coffee DW CCCV implementa um pipeline local de engenharia de dados para ingestão, armazenamento, orquestração e transformação de cotações de café disponibilizadas pela CCCV.

A arquitetura foi desenhada para fins de estudo e portfólio, mas utilizando práticas próximas de um ambiente produtivo.

## Fluxo de dados

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
Consultas analíticas
```

## Orquestração

O Airflow orquestra a execução do pipeline de ingestão.

```text
DAG cccv_coffee_prices_daily
    ↓
start
    ↓
run_cccv_pipeline
    ↓
end
```

## Camadas

### Bronze

Camada responsável por armazenar os dados extraídos da fonte com rastreabilidade.

Tabela principal:

```text
bronze.raw_cccv_daily_prices
```

### Silver

Camada de padronização e preparação dos dados.

Modelo principal:

```text
silver.stg_cccv_coffee_prices
```

### Gold

Camada analítica final.

Modelos:

```text
gold.mart_conilon_daily_prices
gold.mart_coffee_monthly_summary
gold.mart_harvest_comparison
```

## Decisões técnicas

### PostgreSQL como Data Warehouse local

Foi escolhido por ser simples de executar via Docker, amplamente usado e compatível com dbt.

### dbt para transformação

O dbt foi usado para separar transformações SQL do código Python, criar testes de qualidade e organizar modelos analíticos.

### Airflow para orquestração

O Airflow foi usado para transformar o pipeline manual em uma DAG executável e monitorável.

### Safra como dimensão analítica

A fonte CCCV apresenta preços por tipo de café e safra. Por isso, o projeto inclui o campo `harvest_year`, permitindo análises comparativas entre safras.
