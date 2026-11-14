
import pandas as pd


class StoreAnalyzer:
    """
    Performs store and regional performance analysis
    for the SmartMart Retail Analytics System.
    """

    def clean_region_names(self, dataframe):
        """
        Standardise region names by removing extra spaces
        and converting names to title case.
        """

        dataframe = dataframe.copy()

        dataframe["region"] = (
            dataframe["region"]
            .astype("string")
            .str.strip()
            .str.title()
        )

        return dataframe

    def get_store_performance(self, dataframe):
        """
        Calculate and rank store performance based on
        total sales, transactions, and quantity sold.
        """

        dataframe = self.clean_region_names(dataframe)

        sales_data = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        store_performance = (
            sales_data.groupby(
                ["store_id", "store_city", "region"],
                dropna=False
            )
            .agg(
                total_sales=("total_amount", "sum"),
                total_transactions=("transaction_id", "nunique"),
                total_quantity_sold=("quantity", "sum")
            )
            .reset_index()
            .sort_values(
                by="total_sales",
                ascending=False
            )
        )

        store_performance["rank"] = (
            store_performance["total_sales"]
            .rank(method="dense", ascending=False)
            .astype(int)
        )

        return store_performance

    def get_sales_volume_by_store(self, dataframe):
        """
        Calculate sales volume for each store.
        """

        sales_data = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        sales_volume = (
            sales_data.groupby("store_id")
            .agg(
                total_sales=("total_amount", "sum"),
                total_transactions=("transaction_id", "nunique"),
                total_quantity_sold=("quantity", "sum")
            )
            .reset_index()
            .sort_values(
                by="total_quantity_sold",
                ascending=False
            )
        )

        return sales_volume

    def get_regional_performance(self, dataframe):
        """
        Calculate sales performance for each region.
        Region names are standardised to prevent duplicates.
        """

        dataframe = self.clean_region_names(dataframe)

        sales_data = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        regional_performance = (
            sales_data.groupby("region", dropna=False)
            .agg(
                total_sales=("total_amount", "sum"),
                total_transactions=("transaction_id", "nunique"),
                total_quantity_sold=("quantity", "sum"),
                number_of_stores=("store_id", "nunique")
            )
            .reset_index()
            .sort_values(
                by="total_sales",
                ascending=False
            )
        )

        return regional_performance

    def get_store_efficiency(self, dataframe):
        """
        Calculate store efficiency using sales,
        transaction values, and stock information.
        """

        sales_data = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        store_efficiency = (
            sales_data.groupby(["store_id", "store_city"])
            .agg(
                total_sales=("total_amount", "sum"),
                total_transactions=("transaction_id", "nunique"),
                total_quantity_sold=("quantity", "sum"),
                average_transaction_value=("total_amount", "mean"),
                average_stock_on_hand=("stock_on_hand", "mean")
            )
            .reset_index()
        )

        store_efficiency["sales_per_transaction"] = (
            store_efficiency["total_sales"]
            / store_efficiency["total_transactions"].replace(0, pd.NA)
        )

        store_efficiency = store_efficiency.sort_values(
            by="total_sales",
            ascending=False
        )

        return store_efficiency
