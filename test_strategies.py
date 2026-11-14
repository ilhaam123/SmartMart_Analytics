import pandas as pd

from strategies import (
    StrategyContext,
    TotalSalesStrategy,
    BestSellingProductStrategy,
    RegionalSalesStrategy
)


def test_total_sales_strategy():
    dataframe = pd.DataFrame({
        "total_amount": [2000, 3000, 5000]
    })

    analyzer = StrategyContext(TotalSalesStrategy())

    result = analyzer.perform_analysis(dataframe)

    assert result == 10000


def test_best_selling_product_strategy():
    dataframe = pd.DataFrame({
        "product_name": ["Laptop", "Mouse", "Laptop"],
        "quantity": [2, 5, 3]
    })

    analyzer = StrategyContext(BestSellingProductStrategy())

    result = analyzer.perform_analysis(dataframe)

    assert result.index[0] == "Laptop"
    assert result.iloc[0] == 5


def test_regional_sales_strategy():
    dataframe = pd.DataFrame({
        "region": ["West", "East", "West"],
        "total_amount": [4000, 2000, 3000]
    })

    analyzer = StrategyContext(RegionalSalesStrategy())

    result = analyzer.perform_analysis(dataframe)

    assert result["West"] == 7000
    assert result["East"] == 2000


def test_change_strategy():
    dataframe = pd.DataFrame({
        "total_amount": [1000, 2000],
        "region": ["West", "East"]
    })

    analyzer = StrategyContext(TotalSalesStrategy())

    assert analyzer.perform_analysis(dataframe) == 3000

    analyzer.set_strategy(RegionalSalesStrategy())

    result = analyzer.perform_analysis(dataframe)

    assert result["West"] == 1000
    assert result["East"] == 2000
