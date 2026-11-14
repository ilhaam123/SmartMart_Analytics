
import pandas as pd
from seasonal_analyzer import SeasonalAnalyzer


def create_test_data():
    return pd.DataFrame({
        "transaction_id": ["T001", "T002", "T003", "T004"],
        "transaction_datetime": [
            "2025-12-24 10:00:00",
            "2025-12-24 14:00:00",
            "2025-12-25 11:00:00",
            "2025-12-26 12:00:00"
        ],
        "transaction_type": [
            "Sale", "Sale", "Return", "Sale"
        ],
        "total_amount": [
            1000, 1500, -500, 2000
        ],
        "promotion_name": [
            "Christmas Sale",
            "Christmas Sale",
            "Christmas Sale",
            None
        ]
    })


def test_daily_sales_trend():
    analyzer = SeasonalAnalyzer()
    dataframe = create_test_data()

    result = analyzer.get_daily_sales_trend(dataframe)

    assert len(result) == 3
    assert result.loc[0, "net_sales"] == 2500
    assert result.loc[1, "net_sales"] == -500


def test_monthly_sales_trend():
    analyzer = SeasonalAnalyzer()
    dataframe = create_test_data()

    result = analyzer.get_monthly_sales_trend(dataframe)

    assert len(result) == 1
    assert result.loc[0, "month"] == "2025-12"
    assert result.loc[0, "net_sales"] == 4000


def test_promotion_sales():
    analyzer = SeasonalAnalyzer()
    dataframe = create_test_data()

    result = analyzer.get_promotion_sales(dataframe)

    assert len(result) == 1
    assert result.loc[0, "promotion_name"] == "Christmas Sale"
    assert result.loc[0, "total_sales"] == 2000


def test_holiday_sales():
    analyzer = SeasonalAnalyzer()
    dataframe = create_test_data()

    holidays = ["2025-12-25"]

    result = analyzer.get_holiday_sales(
        dataframe, holidays
    )

    holiday_sales = result[
        result["day_type"] == "Public Holiday"
    ]["total_sales"].iloc[0]

    normal_sales = result[
        result["day_type"] == "Normal Day"
    ]["total_sales"].iloc[0]

    assert holiday_sales == -500
    assert normal_sales == 4500
