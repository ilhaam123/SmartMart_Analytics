
import pandas as pd

from data_validator import DataValidator


def test_validate_data():

    validator = DataValidator()

    dataframe = pd.DataFrame({
        "transaction_type": [
            "Sale",
            "Sale",
            "Return"
        ],
        "quantity": [
            2,
            0,
            -5
        ],
        "unit_price": [
            100,
            -200,
            50
        ],
        "total_amount": [
            180,
            50,
            -250
        ],
        "discount_percent": [
            10,
            20,
            110
        ]
    })

    results = validator.validate_data(dataframe)

    assert results["missing_values"] == 0
    assert results["duplicate_records"] == 0
    assert results["invalid_quantities"] == 1
    assert results["invalid_prices"] == 1
    assert results["suspicious_sale_prices"] == 1
    assert results["invalid_total_amounts"] == 0
    assert results["invalid_discounts"] == 1
    assert results["missing_discounts"] == 0
    assert results["invalid_return_quantities"] == 0
    assert results["return_transactions"] == 1
    assert results["mismatched_sale_amounts"] == 1
