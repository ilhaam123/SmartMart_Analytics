
import pandas as pd


class DataProcessor:
    """
    Responsible for cleaning and preparing transaction data.
    """

    def process_data(self, dataframe):
        """
        Cleans the dataset and prepares it for analysis.
        """

        # Create a copy to protect the original dataset
        processed_data = dataframe.copy()

        # 1. Remove exact duplicate records
        processed_data = processed_data.drop_duplicates()

        # 2. Remove records with missing essential values
        essential_columns = [
            "transaction_id",
            "transaction_datetime",
            "quantity",
            "unit_price",
            "total_amount"
        ]

        processed_data = processed_data.dropna(
            subset=essential_columns
        )

        # 3. Convert transaction dates to datetime format
        processed_data["transaction_datetime"] = pd.to_datetime(
            processed_data["transaction_datetime"],
            errors="coerce"
        )

        # 4. Remove records with invalid dates
        processed_data = processed_data.dropna(
            subset=["transaction_datetime"]
        )

        # 5. Reset row numbering
        processed_data = processed_data.reset_index(drop=True)

        return processed_data
