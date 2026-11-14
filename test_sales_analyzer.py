import pandas as pd
from sales_analyzer import SalesAnalyzer


def test_sales_analysis():
    analyzer = SalesAnalyzer()

    # Create sample sales data
    dataframe = pd.DataFrame({
        "transaction_id": [101, 102, 103, 104],
        "product_name": [
            "Laptop", "Mouse", "Laptop", "Keyboard"
        ],
        "quantity": [2, 5, 3, 4],
        "total_amount": [200000, 5000, 300000, 20000],
        "region": [
            "Colombo", "Kandy", "Colombo", "Galle"
        ],
        "product_category": [
            "Electronics", "Accessories",
            "Electronics", "Accessories"
        ]
    })

    # Test total sales
    assert analyzer.get_total_sales(dataframe) == 525000

    # Test transaction count
    assert analyzer.get_total_transactions(dataframe) == 4

    # Test best-selling products
    best_products = analyzer.get_best_selling_products(dataframe)

    assert best_products.index[0] == "Laptop"
    assert best_products.iloc[0] == 5

    # Test regional sales
    regional_sales = analyzer.get_sales_by_region(dataframe)

    assert regional_sales["Colombo"] == 500000
    assert regional_sales["Kandy"] == 5000

    # Test category sales
    category_sales = analyzer.get_sales_by_category(dataframe)

    assert category_sales["Electronics"] == 500000
    assert category_sales["Accessories"] == 25000
