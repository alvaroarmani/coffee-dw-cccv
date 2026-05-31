from decimal import Decimal

from src.loaders.postgres_loader import convert_decimal_to_float


def test_convert_decimal_to_float():
    record = {
        "price_brl": Decimal("984.00"),
        "coffee_type": "conilon",
    }

    result = convert_decimal_to_float(record)

    assert result["price_brl"] == 984.0
    assert result["coffee_type"] == "conilon"


def test_convert_decimal_to_float_does_not_mutate_original_record():
    record = {
        "price_brl": Decimal("984.00"),
        "coffee_type": "conilon",
    }

    result = convert_decimal_to_float(record)

    assert result is not record
    assert record["price_brl"] == Decimal("984.00")
