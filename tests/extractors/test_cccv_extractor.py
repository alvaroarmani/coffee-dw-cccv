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
    result = parse_brazilian_decimal("---")
    assert result is None


def test_extract_reference_month_year():
    text = "Cotação do café referente ao mês de Março de 2026"

    month, year = extract_reference_month_year(text)

    assert month == 3
    assert year == 2026


def test_parse_cccv_current_prices_from_sample_html():
    sample_html = """
    <html>
        <body>
            <h5>Cotação do café referente ao mês de Março de 2026</h5>
            <p>2 1.710,00 1.358,00 984,00</p>
            <p>3 1.708,00 1.365,00 991,00</p>
            <p>4 1.716,00 1.373,00 998,00</p>
            <p>5 1.747,00 1.390,00 1.013,00</p>
            <p>6 1.760,00 1.402,00 1.015,00</p>
            <p>7 ---</p>
        </body>
    </html>
    """

    records = parse_cccv_current_prices(
        html=sample_html,
        source_url="https://www.cccv.org.br/cotacao/",
    )

    assert len(records) == 15

    first_record = records[0]
    assert first_record["price_date"] == "2026-03-02"
    assert first_record["coffee_type"] == "arabica_dura"
    assert first_record["price_brl"] == Decimal("1710.00")

    conilon_record = records[2]
    assert conilon_record["price_date"] == "2026-03-02"
    assert conilon_record["coffee_type"] == "conilon"
    assert conilon_record["price_brl"] == Decimal("984.00")
