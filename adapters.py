import pandas as pd
from pathlib import Path


class ExcelLibraryAdapter:
    """
    Adapter that connects the external Pandas Excel-reading
    functionality with the application's internal interface.
    """

    def read_excel_file(self, file_path):
        """
        Reads an Excel file using Pandas and returns
        the data as a DataFrame.
        """

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Excel file not found: {file_path}"
            )

        if file_path.suffix.lower() != ".xlsx":
            raise ValueError(
                "Only .xlsx files are supported."
            )

        return pd.read_excel(
            file_path,
            engine="openpyxl"
        )


class ExcelReaderAdapter:
    """
    Adapts the external Excel library adapter
    to the application's internal read_data interface.
    """

    def __init__(self, excel_adapter=None):
        self.excel_adapter = (
            excel_adapter or ExcelLibraryAdapter()
        )

    def read_data(self, file_path):
        """
        Provides a standard method for reading Excel data.
        """

        return self.excel_adapter.read_excel_file(file_path)
