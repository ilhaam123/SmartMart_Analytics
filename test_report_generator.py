import pandas as pd
from report_generator import ReportGenerator


def test_generate_report():
    generator = ReportGenerator()

    dataframe = pd.DataFrame({
        "transaction_id": [101, 102, 103],
        "total_amount": [2000, 3000, 5000]
    })

    analysis_results = {
        "total_sales": 10000,
        "total_transactions": 3,
        "best_selling_products": pd.Series(
            [5, 3],
            index=["Laptop", "Mouse"]
        ),
        "sales_by_region": pd.Series(
            [6000, 4000],
            index=["Colombo", "Kandy"]
        ),
        "sales_by_category": pd.Series(
            [7000, 3000],
            index=["Electronics", "Accessories"]
        )
    }

    report = generator.generate_report(
        dataframe,
        analysis_results
    )

    assert report["report_title"] == (
        "SmartMart Sales Analysis Report"
    )
    assert report["total_records"] == 3
    assert report["total_sales"] == 10000
    assert report["total_transactions"] == 3

    assert report["best_selling_products"]["Laptop"] == 5
    assert report["sales_by_region"]["Colombo"] == 6000
    assert report["sales_by_category"]["Electronics"] == 7000

    assert "generated_at" in report
