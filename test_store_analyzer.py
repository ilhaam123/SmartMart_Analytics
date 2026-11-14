
import pandas as pd
from store_analyzer import StoreAnalyzer


def create_sample_data():
    return pd.DataFrame({
        "transaction_id": [1, 2, 3, 4, 5, 6],
        "transaction_type": [
            "Sale", "Sale", "Sale", "Sale", "Return", "Sale"
        ],
        "store_id": [
            "S001", "S001", "S002", "S002", "S001", "S003"
        ],
        "store_city": [
            "Colombo", "Colombo", "Kandy", "Kandy", "Colombo", "Galle"
        ],
        "region": [
            "Western", "Western", "Central", "Central",
            "Western", "Southern"
        ],
        "total_amount": [5000, 3000, 7000, 2000, -1000, 4000],
        "quantity": [5, 3, 7, 2, -1, 4],
        "stock_on_hand": [50, 45, 60, 55, 50, 40]
    })


def test_store_performance():
    analyzer = StoreAnalyzer()
    result = analyzer.get_store_performance(create_sample_data())

    assert len(result) == 3
    assert result.iloc[0]["store_id"] == "S002"
    assert result.iloc[0]["total_sales"] == 9000
    assert result.iloc[0]["rank"] == 1


def test_sales_volume_by_store():
    analyzer = StoreAnalyzer()
    result = analyzer.get_sales_volume_by_store(create_sample_data())

    assert len(result) == 3
    assert result.iloc[0]["store_id"] == "S002"
    assert result.iloc[0]["total_quantity_sold"] == 9


def test_regional_performance():
    analyzer = StoreAnalyzer()
    result = analyzer.get_regional_performance(create_sample_data())

    assert len(result) == 3
    assert result.iloc[0]["region"] == "Central"
    assert result.iloc[0]["total_sales"] == 9000
    assert result.iloc[0]["number_of_stores"] == 1


def test_store_efficiency():
    analyzer = StoreAnalyzer()
    result = analyzer.get_store_efficiency(create_sample_data())

    assert len(result) == 3
    assert result.iloc[0]["store_id"] == "S002"
    assert result.iloc[0]["sales_per_transaction"] == 4500
