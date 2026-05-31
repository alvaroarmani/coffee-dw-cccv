# Decisões técnicas

## Uso de PostgreSQL

O PostgreSQL foi escolhido como banco principal do Data Warehouse local por ser simples de executar via Docker, amplamente utilizado e compatível com dbt.

## Uso de arquitetura Medallion

O projeto utiliza as camadas Bronze, Silver e Gold para separar responsabilidades:

- Bronze: dados brutos ou semitratados
- Silver: dados padronizados e validados
- Gold: dados analíticos prontos para consumo

## Uso de Airflow

O Airflow foi escolhido para orquestrar o pipeline de ingestão e transformação, permitindo acompanhar execuções, falhas e histórico de processamento.

## Uso de dbt

O dbt foi escolhido para separar transformações SQL do código Python, criar modelos analíticos, documentar fontes e aplicar testes de qualidade.

## Safra como dimensão analítica

A página da CCCV apresenta cotações por tipo de café e safra. Por isso, o projeto modela `harvest_year` como uma dimensão importante.

Essa decisão permite análises como:

- comparação entre safras
- identificação de início de cotação da safra futura
- diferença percentual entre safra atual e futura
- análise mensal por tipo de café e safra

## CI com dados controlados

O GitHub Actions usa dados de exemplo para validar os modelos dbt. Isso evita dependência da página externa da CCCV durante o CI.
