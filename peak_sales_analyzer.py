
import pandas as pd


class PeakSalesAnalyzer:
    """
    Analyses peak shopping periods and customer transactions.
    """

    def get_peak_sales_heatmap(self, dataframe):
        """
        Counts Sale transactions by weekday and hour
        across all stores.
        """

        sales_data = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        sales_data["transaction_datetime"] = pd.to_datetime(
            sales_data["transaction_datetime"],
            errors="coerce"
        )

        sales_data = sales_data.dropna(
            subset=["transaction_datetime"]
        )

        sales_data["weekday"] = (
            sales_data["transaction_datetime"].dt.day_name()
        )

        sales_data["hour"] = (
            sales_data["transaction_datetime"].dt.hour
        )

        weekday_order = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        heatmap_data = pd.crosstab(
            sales_data["weekday"],
            sales_data["hour"]
        )

        heatmap_data = heatmap_data.reindex(
            index=weekday_order,
            columns=range(24),
            fill_value=0
        )

        return heatmap_data

    def search_customer(self, dataframe, customer_id):
        """
        Retrieves transaction records for a customer.
        """

        if not customer_id or not str(customer_id).strip():
            return pd.DataFrame()

        customer_data = dataframe[
            dataframe["customer_id"].astype("string").str.strip()
            == str(customer_id).strip()
        ].copy()

        return customer_data.reset_index(drop=True)
