from facade import SmartMartFacade


def test_facade_process_dataset():
    facade = SmartMartFacade()

    results = facade.process_dataset(
        "data/smartretail_transactions.xlsx"
    )

    # Check that all expected result sections exist
    assert "validation_results" in results
    assert "processed_data" in results
    assert "analysis_results" in results
    assert "report" in results

    # Check the processed dataset
    assert not results["processed_data"].empty

    # Check the generated report
    assert results["report"]["report_title"] == (
        "SmartMart Sales Analysis Report"
    )

    assert results["report"]["total_records"] > 0
    assert results["report"]["total_transactions"] > 0


def test_facade_initializes_components():
    facade = SmartMartFacade()

    assert facade.data_reader is not None
    assert facade.data_validator is not None
    assert facade.data_processor is not None
    assert facade.sales_analyzer is not None
    assert facade.report_generator is not None
