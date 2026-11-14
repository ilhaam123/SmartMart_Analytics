
import pandas as pd
import pytest

from inventory_analyzer import InventoryAnalyzer


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "store_id": ["ST100", "ST100", "ST100", "ST101", "ST101"],
        "product_name": [
            "Bread", "Bread", "Milk", "Bread", "Milk"
        ],
        "product_category": [
            "Bakery", "Bakery", "Dairy", "Bakery", "Dairy"
        ],
        "transaction_datetime": [
            "2024-01-01 10:00:00",
            "2024-01-02 10:00:00",
            "2024-01-02 11:00:00",
            "2024-01-02 12:00:00",
            "2024-01-02 13:00:00"
        ],
        "stock_on_hand": [50, 10, 0, 40, 30],
        "reorder_level": [20, 20, 15, 20, 30]
    })


@pytest.fixture
def analyzer():
    return InventoryAnalyzer()


def test_get_latest_stock(analyzer, sample_data):
    result = analyzer.get_latest_stock(sample_data)

    assert len(result) == 4

    bread_st100 = result[
        (result["store_id"] == "ST100") &
        (result["product_name"] == "Bread")
    ]

    assert bread_st100.iloc[0]["stock_on_hand"] == 10


def test_get_stock_status(analyzer, sample_data):
    result = analyzer.get_stock_status(sample_data)

    assert len(result) == 4

    statuses = set(result["stock_status"])

    assert "Healthy" in statuses
    assert "Reorder Required" in statuses
    assert "Out of Stock" in statuses


def test_get_inventory_summary(analyzer, sample_data):
    result = analyzer.get_inventory_summary(sample_data)

    assert result["total_products"] == 2
    assert result["total_product_store_combinations"] == 4
    assert result["out_of_stock"] == 1
    assert result["reorder_required"] == 2
    assert result["healthy_stock"] == 1
    assert result["total_stock_units"] == 80


def test_get_low_stock_products(analyzer, sample_data):
    result = analyzer.get_low_stock_products(sample_data)

    assert len(result) == 2
    assert (result["stock_on_hand"] > 0).all()
    assert (
        result["stock_on_hand"] <= result["reorder_level"]
    ).all()


def test_get_out_of_stock_products(analyzer, sample_data):
    result = analyzer.get_out_of_stock_products(sample_data)

    assert len(result) == 1
    assert (result["stock_on_hand"] == 0).all()


def test_get_stock_by_store(analyzer, sample_data):
    result = analyzer.get_stock_by_store(sample_data)

    assert len(result) == 2
    assert "total_stock_units" in result.columns
    assert "low_stock_count" in result.columns
    assert "out_of_stock_count" in result.columns


def test_get_stock_by_category(analyzer, sample_data):
    result = analyzer.get_stock_by_category(sample_data)

    assert len(result) == 2
    assert "product_category" in result.columns
    assert "total_stock_units" in result.columns


def test_missing_required_columns(analyzer):
    invalid_data = pd.DataFrame({
        "store_id": ["ST100"],
        "product_name": ["Bread"]
    })

    with pytest.raises(ValueError):
        analyzer.get_latest_stock(invalid_data)
