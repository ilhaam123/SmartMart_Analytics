
import pandas as pd

from customer_analyzer import CustomerAnalyzer


def create_test_data():
    return pd.DataFrame({
        "transaction_id": [
            "T001", "T002", "T003", "T004", "T005",
            "T006", "T007", "T008", "T009", "T010",
            "T011", "T012"
        ],
        "transaction_type": [
            "Sale", "Sale", "Sale", "Sale",
            "Sale", "Sale", "Sale", "Sale",
            "Sale", "Sale", "Sale", "Return"
        ],
        "customer_id": [
            "C001", "C001", "C002", "C003",
            "C003", "C003", "C003", "C003",
            "C003", "C004", "C004", "C001"
        ],
        "customer_age": [
            22, 22, 30, 40, 40, 40,
            40, 40, 40, 60, 60, 22
        ],
        "customer_city": [
            "Colombo", "Colombo", "Kandy", "Galle",
            "Galle", "Galle", "Galle", "Galle",
            "Galle", "Jaffna", "Jaffna", "Colombo"
        ],
        "total_amount": [
            1000, 1500, 2000, 500, 600, 700,
            800, 900, 1000, 3000, 3500, -500
        ]
    })


def test_customer_frequency():
    analyzer = CustomerAnalyzer()
    data = create_test_data()

    result = analyzer.get_customer_frequency(data)

    assert result["One-time"] == 1
    assert result["Occasional"] == 2
    assert result["Frequent"] == 1


def test_customer_clusters():
    analyzer = CustomerAnalyzer()
    data = create_test_data()

    result = analyzer.get_customer_clusters(data)

    assert not result.empty
    assert "purchase_frequency" in result.columns
    assert "average_basket_value" in result.columns
    assert "cluster" in result.columns


def test_customer_age_groups():
    analyzer = CustomerAnalyzer()
    data = create_test_data()

    result = analyzer.get_customer_age_groups(data)

    assert not result.empty
    assert "age_group" in result.columns
    assert "customers" in result.columns
    assert "sales_amount" in result.columns


def test_top_customer_cities():
    analyzer = CustomerAnalyzer()
    data = create_test_data()

    result = analyzer.get_top_customer_cities(data)

    assert not result.empty
    assert result.iloc[0]["customer_city"] == "Jaffna"
    assert result.iloc[0]["total_sales"] == 6500
