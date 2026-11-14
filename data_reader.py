import pandas as pd
from pathlib import Path


class ExcelDataReader:
    """
    Responsible for reading Excel datasets.
    """

    def read_data(self, file_path):
        """
        Reads an Excel file and returns its data as a DataFrame.
        """

        file_path = Path(file_path)

        # Check whether the file exists
        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        # Check the file format
        if file_path.suffix.lower() != ".xlsx":
            raise ValueError(
                "Unsupported file format. Please select an .xlsx file."
            )

        # Read Excel data
        dataframe = pd.read_excel(file_path, engine="openpyxl")

        return dataframe

    def get_dataset_summary(self, dataframe):
        """
        Returns basic information about the dataset.
        """

        summary = {
            "total_records": len(dataframe),
            "total_columns": len(dataframe.columns),
            "column_names": list(dataframe.columns),
            "missing_values": int(dataframe.isnull().sum().sum())
        }

        return summary
