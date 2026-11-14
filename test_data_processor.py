import pandas as pd
from data_processor import DataProcessor


def test_process_data():
    processor = DataProcessor()

    # Create a sample dataset
    dataframe = pd.DataFrame({
        "transaction_id": [101, 102, 102, 103],
        "transaction_datetime": [
            "2026-01-01",
            "2026-01-02",
            "2026-01-02",
            "invalid_date"
        ],
        "quantity": [2, 3, 3, 4],
        "unit_price": [100, 200, 200, 150],
        "total_amount": [200, 600, 600, 600]
    })

    processed_data = processor.process_data(dataframe)

    # Check duplicate removal
    assert len(processed_data) == 2

    # Check that transaction IDs are correct
    assert list(processed_data["transaction_id"]) == [101, 102]

    # Check that dates are converted
    assert pd.api.types.is_datetime64_any_dtype(
        processed_data["transaction_datetime"]
    )

    # Check that the index is reset
    assert list(processed_data.index) == [0, 1]
