with source as (

    select
        id,
        price_date,
        coffee_type,
        coffee_description,
        harvest_year,
        price_brl,
        source_url,
        extracted_at,
        loaded_at
    from {{ source('bronze', 'raw_cccv_daily_prices') }}

),

renamed as (

    select
        id as raw_price_id,
        price_date,
        coffee_type,
        coffee_description,
        harvest_year,
        price_brl::numeric(12, 2) as price_brl,
        source_url,
        extracted_at,
        loaded_at
    from source

)

select *
from renamed