from factories import (
    ExcelDataReaderFactory,
    DataReaderFactory
)


def test_excel_data_reader_factory():
    factory = ExcelDataReaderFactory()

    reader = factory.create_reader()

    assert reader is not None
    assert reader.__class__.__name__ == "ExcelDataReader"
    assert hasattr(reader, "read_data")


def test_factory_implements_abstract_class():
    factory = ExcelDataReaderFactory()

    assert isinstance(factory, DataReaderFactory)
