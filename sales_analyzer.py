class SalesAnalyzer:
    """
    Performs sales analysis on processed SmartMart transaction data.
    """

    def get_total_sales(self, dataframe):
        """Calculates total net sales."""

        return round(
            dataframe["total_amount"].sum(),
            2
        )

    def get_total_transactions(self, dataframe):
        """Calculates the number of unique transactions."""

        return int(
            dataframe["transaction_id"].nunique()
        )

    def get_best_selling_products(self, dataframe, limit=5):
        """Identifies the best-selling products based on quantity."""

        product_sales = (
            dataframe.groupby("product_name")["quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(limit)
        )

        return product_sales

    def get_sales_by_region(self, dataframe):
        """
        Calculates net sales by region.
        Standardises region names to avoid duplicate groups
        caused by inconsistent capitalisation or extra spaces.
        """

        cleaned_data = dataframe.copy()

        cleaned_data["region"] = (
            cleaned_data["region"]
            .astype("string")
            .str.strip()
            .str.title()
        )

        return (
            cleaned_data.groupby("region")["total_amount"]
            .sum()
            .sort_values(ascending=False)
        )

    def get_sales_by_category(self, dataframe):
        """Calculates net sales by product category."""

        return (
            dataframe.groupby("product_category")["total_amount"]
            .sum()
            .sort_values(ascending=False)
        )
