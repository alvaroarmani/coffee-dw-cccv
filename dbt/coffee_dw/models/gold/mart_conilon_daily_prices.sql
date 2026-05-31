select
    price_date,
    coffee_type,
    coffee_description,
    harvest_year,
    price_brl,
    source_url,
    extracted_at,
    loaded_at
from {{ ref('stg_cccv_coffee_prices') }}
where coffee_type = 'conilon'