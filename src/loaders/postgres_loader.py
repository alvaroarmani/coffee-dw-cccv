import os
from decimal import Decimal
from typing import Iterable

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv()


def get_postgres_connection_url() -> str:
    """
    Monta a URL de conexão do PostgreSQL usando as variáveis do .env.

    Quando rodamos localmente fora do Docker, usamos localhost.
    Dentro do Docker, o host será postgres.
    """
    host = os.getenv("POSTGRES_LOCAL_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "coffee_dw")
    user = os.getenv("POSTGRES_USER", "coffee_user")
    password = os.getenv("POSTGRES_PASSWORD", "coffee_password")

    return f"postgresql+pg8000://{user}:{password}@{host}:{port}/{database}"


def get_engine() -> Engine:
    """
    Cria uma engine SQLAlchemy para conexão com o PostgreSQL.
    """
    connection_url = get_postgres_connection_url()
    print(f"Conectando ao PostgreSQL em: {connection_url}")
    return create_engine(connection_url)


def convert_decimal_to_float(record: dict) -> dict:
    """
    Converte Decimal para float para facilitar o bind no SQLAlchemy.
    """
    converted_record = record.copy()

    if isinstance(converted_record.get("price_brl"), Decimal):
        converted_record["price_brl"] = float(converted_record["price_brl"])

    return converted_record


def load_raw_cccv_daily_prices(
    records: Iterable[dict], engine: Engine | None = None
) -> int:
    """
    Carrega registros na tabela bronze.raw_cccv_daily_prices.

    Usa ON CONFLICT para evitar duplicidades quando o mesmo dado já existe.
    """
    records = list(records)

    if not records:
        return 0

    prepared_records = [convert_decimal_to_float(record) for record in records]

    should_dispose_engine = False

    if engine is None:
        engine = get_engine()
        should_dispose_engine = True

    insert_sql = text("""
        INSERT INTO bronze.raw_cccv_daily_prices (
            price_date,
            coffee_type,
            coffee_description,
            harvest_year,
            price_brl,
            source_url,
            extracted_at
        )
        VALUES (
            :price_date,
            :coffee_type,
            :coffee_description,
            :harvest_year,
            :price_brl,
            :source_url,
            :extracted_at
        )
        ON CONFLICT (price_date, coffee_type, harvest_year, source_url)
        DO UPDATE SET
            coffee_description = EXCLUDED.coffee_description,
            price_brl = EXCLUDED.price_brl,
            extracted_at = EXCLUDED.extracted_at,
            loaded_at = CURRENT_TIMESTAMP
        """)
    with engine.begin() as connection:
        result = connection.execute(insert_sql, prepared_records)

    if should_dispose_engine:
        engine.dispose()

    return result.rowcount
