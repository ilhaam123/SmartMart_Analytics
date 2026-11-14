from data_reader import ExcelDataReader


def test_read_smartmart_dataset():
    reader = ExcelDataReader()

    dataframe = reader.read_data(
        "data/smartretail_transactions.xlsx"
    )

    assert not dataframe.empty
    assert len(dataframe.columns) == 22
    assert "transaction_id" in dataframe.columns
    assert "total_amount" in dataframe.columns
