select
    date_trunc('month', price_date)::date as reference_month,
    coffee_type,
    coffee_description,
    harvest_year,
    count(*) as total_quotes,
    min(price_brl) as min_price_brl,
    max(price_brl) as max_price_brl,
    avg(price_brl)::numeric(12, 2) as avg_price_brl
from {{ ref('stg_cccv_coffee_prices') }}
group by
    date_trunc('month', price_date)::date,
    coffee_type,
    coffee_description,
    harvest_year