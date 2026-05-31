DROP TABLE IF EXISTS bronze.raw_cccv_daily_prices CASCADE;

CREATE TABLE bronze.raw_cccv_daily_prices (
    id BIGSERIAL PRIMARY KEY,
    price_date DATE NOT NULL,
    coffee_type VARCHAR(50) NOT NULL,
    coffee_description VARCHAR(150) NOT NULL,
    harvest_year VARCHAR(20) NOT NULL,
    price_brl NUMERIC(12, 2) NOT NULL,
    source_url TEXT NOT NULL,
    extracted_at TIMESTAMP NOT NULL,
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_raw_cccv_daily_prices UNIQUE (
        price_date,
        coffee_type,
        harvest_year,
        source_url
    )
);