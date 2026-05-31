from decimal import Decimal

from src.extractors.cccv_extractor import (
    extract_reference_month_year,
    parse_brazilian_decimal,
    parse_cccv_current_prices,
)


def test_parse_brazilian_decimal_with_thousand_separator():
    result = parse_brazilian_decimal("1.013,00")

    assert result == Decimal("1013.00")


def test_parse_brazilian_decimal_without_thousand_separator():
    result = parse_brazilian_decimal("984,00")

    assert result == Decimal("984.00")


def test_parse_brazilian_decimal_with_empty_value():
    result = parse_brazilian_decimal("-")

    assert result is None


def test_parse_brazilian_decimal_with_old_empty_value():
    result = parse_brazilian_decimal("---")

    assert result is None


def test_extract_reference_month_year():
    text = "Cotação do café referente ao mês de Maio de 2026"

    month, year = extract_reference_month_year(text)

    assert month == 5
    assert year == 2026


def test_parse_cccv_current_prices_from_sample_html():
    sample_html = """
    <html>
        <body>
            <h5>Cotação do café referente ao mês de Maio de 2026</h5>
            <p>4 1.643,00 1.130,00 - - 873,00 -</p>
            <p>5 1.653,00 1.175,00 - - 869,00 -</p>
            <p>6 1.629,00 1.140,00 - - 865,00 -</p>
        </body>
    </html>
    """

    records = parse_cccv_current_prices(
        html=sample_html,
        source_url="https://www.cccv.org.br/cotacao/",
    )

    assert len(records) == 9

    first_day_records = [
        record for record in records if record["price_date"] == "2026-05-04"
    ]

    prices_by_type_and_harvest = {
        (record["coffee_type"], record["harvest_year"]): record["price_brl"]
        for record in first_day_records
    }

    assert prices_by_type_and_harvest[("arabica_dura", "2025/2026")] == Decimal(
        "1643.00"
    )
    assert prices_by_type_and_harvest[("arabica_rio", "2025/2026")] == Decimal(
        "1130.00"
    )
    assert prices_by_type_and_harvest[("conilon", "2025/2026")] == Decimal("873.00")


def test_parse_cccv_current_prices_with_future_harvest_values():
    sample_html = """
    <html>
        <body>
            <h5>Cotação do café referente ao mês de Maio de 2026</h5>
            <p>20 1.600,00 1.100,00 1.500,00 1.050,00 850,00 830,00</p>
        </body>
    </html>
    """

    records = parse_cccv_current_prices(
        html=sample_html,
        source_url="https://www.cccv.org.br/cotacao/",
    )

    assert len(records) == 6

    prices_by_type_and_harvest = {
        (record["coffee_type"], record["harvest_year"]): record["price_brl"]
        for record in records
    }

    assert prices_by_type_and_harvest[("arabica_dura", "2025/2026")] == Decimal(
        "1600.00"
    )
    assert prices_by_type_and_harvest[("arabica_rio", "2025/2026")] == Decimal(
        "1100.00"
    )
    assert prices_by_type_and_harvest[("arabica_dura", "2026/2027")] == Decimal(
        "1500.00"
    )
    assert prices_by_type_and_harvest[("arabica_rio", "2026/2027")] == Decimal(
        "1050.00"
    )
    assert prices_by_type_and_harvest[("conilon", "2025/2026")] == Decimal("850.00")
    assert prices_by_type_and_harvest[("conilon", "2026/2027")] == Decimal("830.00")
