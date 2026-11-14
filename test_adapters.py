import pandas as pd
import pytest

from adapters import (
    ExcelLibraryAdapter,
    ExcelReaderAdapter
)


def test_excel_reader_adapter(tmp_path):
    # Create a temporary Excel dataset
    sample_data = pd.DataFrame({
        "transaction_id": [101, 102, 103],
        "total_amount": [2000, 3000, 5000]
    })

    file_path = tmp_path / "sample.xlsx"

    sample_data.to_excel(
        file_path,
        index=False,
        engine="openpyxl"
    )

    # Create the adapter
    adapter = ExcelReaderAdapter()

    # Read the Excel file
    result = adapter.read_data(file_path)

    assert len(result) == 3
    assert list(result.columns) == [
        "transaction_id",
        "total_amount"
    ]


def test_excel_library_adapter(tmp_path):
    sample_data = pd.DataFrame({
        "product_name": ["Laptop", "Mouse"],
        "quantity": [2, 5]
    })

    file_path = tmp_path / "products.xlsx"

    sample_data.to_excel(
        file_path,
        index=False,
        engine="openpyxl"
    )

    adapter = ExcelLibraryAdapter()

    result = adapter.read_excel_file(file_path)

    assert len(result) == 2
    assert "product_name" in result.columns


def test_missing_excel_file():
    adapter = ExcelReaderAdapter()

    with pytest.raises(FileNotFoundError):
        adapter.read_data("missing_file.xlsx")


def test_unsupported_file_format(tmp_path):
    file_path = tmp_path / "sample.csv"
    file_path.write_text("id,name\n1,Laptop")

    adapter = ExcelReaderAdapter()

    with pytest.raises(ValueError):
        adapter.read_data(file_path)
