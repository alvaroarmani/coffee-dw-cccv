# Queries analíticas

Este documento contém exemplos de consultas analíticas sobre os modelos Gold.

## Evolução diária do Conilon por safra

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

## Resumo mensal por tipo de café e safra

```sql
SELECT
    reference_month,
    coffee_type,
    harvest_year,
    total_quotes,
    min_price_brl,
    max_price_brl,
    avg_price_brl
FROM gold.mart_coffee_monthly_summary
ORDER BY
    reference_month,
    coffee_type,
    harvest_year;
```

## Comparação entre safras

```sql
SELECT
    price_date,
    coffee_type,
    price_2025_2026,
    price_2026_2027,
    price_diff_brl,
    price_diff_pct
FROM gold.mart_harvest_comparison
ORDER BY
    price_date,
    coffee_type;
```

## Maior preço por tipo de café

```sql
SELECT
    coffee_type,
    harvest_year,
    MAX(price_brl) AS max_price_brl
FROM silver.stg_cccv_coffee_prices
GROUP BY
    coffee_type,
    harvest_year
ORDER BY
    max_price_brl DESC;
```

## Média de preço por tipo de café

```sql
SELECT
    coffee_type,
    harvest_year,
    AVG(price_brl)::numeric(12, 2) AS avg_price_brl
FROM silver.stg_cccv_coffee_prices
GROUP BY
    coffee_type,
    harvest_year
ORDER BY
    coffee_type,
    harvest_year;
```
