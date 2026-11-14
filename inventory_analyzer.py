
import pandas as pd


class InventoryAnalyzer:
    """
    Analyses the latest recorded inventory levels
    for each product at each store.
    """

    def get_latest_stock(self, dataframe):
        required_columns = [
            "store_id",
            "product_name",
            "transaction_datetime",
            "stock_on_hand",
            "reorder_level"
        ]

        missing_columns = [
            column for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        stock_data = dataframe.copy()

        stock_data["transaction_datetime"] = pd.to_datetime(
            stock_data["transaction_datetime"],
            errors="coerce"
        )

        stock_data["stock_on_hand"] = pd.to_numeric(
            stock_data["stock_on_hand"], errors="coerce"
        )

        stock_data["reorder_level"] = pd.to_numeric(
            stock_data["reorder_level"], errors="coerce"
        )

        stock_data = stock_data.dropna(
            subset=[
                "store_id",
                "product_name",
                "transaction_datetime",
                "stock_on_hand",
                "reorder_level"
            ]
        )

        stock_data = stock_data.sort_values(
            "transaction_datetime"
        )

        latest_stock = stock_data.drop_duplicates(
            subset=["store_id", "product_name"],
            keep="last"
        ).copy()

        return latest_stock.reset_index(drop=True)

    def get_stock_status(self, dataframe):
        latest_stock = self.get_latest_stock(dataframe)

        latest_stock["stock_status"] = "Healthy"

        latest_stock.loc[
            latest_stock["stock_on_hand"]
            <= latest_stock["reorder_level"],
            "stock_status"
        ] = "Reorder Required"

        latest_stock.loc[
            latest_stock["stock_on_hand"] == 0,
            "stock_status"
        ] = "Out of Stock"

        return latest_stock

    def get_inventory_summary(self, dataframe):
        stock_data = self.get_stock_status(dataframe)

        summary = {
            "total_products": stock_data["product_name"].nunique(),
            "total_product_store_combinations": len(stock_data),
            "out_of_stock": (
                stock_data["stock_status"] == "Out of Stock"
            ).sum(),
            "reorder_required": (
                stock_data["stock_status"] == "Reorder Required"
            ).sum(),
            "healthy_stock": (
                stock_data["stock_status"] == "Healthy"
            ).sum(),
            "total_stock_units": stock_data["stock_on_hand"].sum()
        }

        return summary

    def get_low_stock_products(self, dataframe):
        stock_data = self.get_stock_status(dataframe)

        low_stock = stock_data[
            stock_data["stock_status"] == "Reorder Required"
        ].copy()

        return low_stock.sort_values(
            "stock_on_hand", ascending=True
        ).reset_index(drop=True)

    def get_out_of_stock_products(self, dataframe):
        stock_data = self.get_stock_status(dataframe)

        out_of_stock = stock_data[
            stock_data["stock_status"] == "Out of Stock"
        ].copy()

        return out_of_stock.reset_index(drop=True)

    def get_stock_by_store(self, dataframe):
        stock_data = self.get_stock_status(dataframe)

        store_summary = (
            stock_data.groupby("store_id")
            .agg(
                total_stock_units=("stock_on_hand", "sum"),
                product_count=("product_name", "nunique"),
                low_stock_count=(
                    "stock_status",
                    lambda values: (values == "Reorder Required").sum()
                ),
                out_of_stock_count=(
                    "stock_status",
                    lambda values: (values == "Out of Stock").sum()
                )
            )
            .reset_index()
        )

        return store_summary.sort_values(
            "total_stock_units", ascending=False
        ).reset_index(drop=True)

    def get_stock_by_category(self, dataframe):
        stock_data = self.get_stock_status(dataframe)

        if "product_category" not in stock_data.columns:
            raise ValueError("Missing product_category column")

        category_summary = (
            stock_data.groupby("product_category")
            .agg(
                total_stock_units=("stock_on_hand", "sum"),
                product_count=("product_name", "nunique"),
                low_stock_count=(
                    "stock_status",
                    lambda values: (values == "Reorder Required").sum()
                ),
                out_of_stock_count=(
                    "stock_status",
                    lambda values: (values == "Out of Stock").sum()
                )
            )
            .reset_index()
            .sort_values(
                "total_stock_units", ascending=False
            )
        )

        return category_summary.reset_index(drop=True)
