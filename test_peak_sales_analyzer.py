
import pandas as pd

from peak_sales_analyzer import PeakSalesAnalyzer


def test_peak_sales_heatmap():
    analyzer = PeakSalesAnalyzer()

    dataframe = pd.DataFrame({
        "transaction_type": [
            "Sale", "Sale", "Sale", "Return"
        ],
        "transaction_datetime": [
            "2026-01-05 09:30:00",
            "2026-01-05 09:45:00",
            "2026-01-06 14:00:00",
            "2026-01-05 09:50:00"
        ],
        "transaction_id": [
            "T001", "T002", "T003", "T004"
        ]
    })

    result = analyzer.get_peak_sales_heatmap(dataframe)

    assert result.loc["Monday", 9] == 2
    assert result.loc["Tuesday", 14] == 1
    assert result.loc["Monday", 9] != 3

    assert result.shape == (7, 24)


def test_customer_search():
    analyzer = PeakSalesAnalyzer()

    dataframe = pd.DataFrame({
        "customer_id": ["C001", "C002", "C001"],
        "transaction_id": ["T001", "T002", "T003"]
    })

    result = analyzer.search_customer(dataframe, "C001")

    assert len(result) == 2
    assert all(result["customer_id"] == "C001")


def test_customer_search_no_match():
    analyzer = PeakSalesAnalyzer()

    dataframe = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "transaction_id": ["T001", "T002"]
    })

    result = analyzer.search_customer(dataframe, "C999")

    assert result.empty
