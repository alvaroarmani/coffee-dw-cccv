with daily_prices as (

    select
        price_date,
        coffee_type,
        coffee_description,
        harvest_year,
        price_brl
    from {{ ref('stg_cccv_coffee_prices') }}

),

pivoted as (

    select
        price_date,
        coffee_type,
        max(coffee_description) as coffee_description,
        max(case when harvest_year = '2025/2026' then price_brl end) as price_2025_2026,
        max(case when harvest_year = '2026/2027' then price_brl end) as price_2026_2027
    from daily_prices
    group by
        price_date,
        coffee_type

),

calculated as (

    select
        price_date,
        coffee_type,
        coffee_description,
        price_2025_2026,
        price_2026_2027,
        case
            when price_2025_2026 is not null
             and price_2026_2027 is not null
            then price_2026_2027 - price_2025_2026
        end as price_diff_brl,
        case
            when price_2025_2026 is not null
             and price_2026_2027 is not null
             and price_2025_2026 <> 0
            then ((price_2026_2027 - price_2025_2026) / price_2025_2026 * 100)::numeric(12, 2)
        end as price_diff_pct
    from pivoted

)

select *
from calculated