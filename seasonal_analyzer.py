
import pandas as pd


class SeasonalAnalyzer:
    """
    Analyses daily sales trends, seasonal patterns,
    promotions, and public holiday sales.
    """

    def get_daily_sales_trend(self, dataframe):
        """
        Calculates daily net sales using Sale and Return transactions.
        """

        data = dataframe.copy()

        data["transaction_datetime"] = pd.to_datetime(
            data["transaction_datetime"],
            errors="coerce"
        )

        data = data.dropna(
            subset=["transaction_datetime", "total_amount"]
        )

        data["net_amount"] = data["total_amount"]

        daily_sales = (
            data.groupby(
                data["transaction_datetime"].dt.date
            )["net_amount"]
            .sum()
            .reset_index()
        )

        daily_sales.columns = ["date", "net_sales"]

        return daily_sales

    def get_monthly_sales_trend(self, dataframe):
        """
        Calculates monthly net sales.
        """

        data = dataframe.copy()

        data["transaction_datetime"] = pd.to_datetime(
            data["transaction_datetime"],
            errors="coerce"
        )

        data = data.dropna(
            subset=["transaction_datetime", "total_amount"]
        )

        data["month"] = (
            data["transaction_datetime"].dt.to_period("M")
        )

        monthly_sales = (
            data.groupby("month")["total_amount"]
            .sum()
            .reset_index()
        )

        monthly_sales["month"] = (
            monthly_sales["month"].astype(str)
        )

        monthly_sales.columns = ["month", "net_sales"]

        return monthly_sales

    def get_promotion_sales(self, dataframe):
        """
        Compares sales from promotional and
        non-promotional transactions.
        """

        data = dataframe.copy()

        data = data.dropna(
            subset=["total_amount", "promotion_name"]
        )

        data["promotion_name"] = (
            data["promotion_name"].astype(str).str.strip()
        )

        data = data[data["promotion_name"] != ""]

        promotion_sales = (
            data.groupby("promotion_name")
            .agg(
                total_sales=("total_amount", "sum"),
                total_transactions=("transaction_id", "nunique")
            )
            .sort_values("total_sales", ascending=False)
            .reset_index()
        )

        return promotion_sales

    def get_holiday_sales(self, dataframe, holiday_dates):
        """
        Compares sales on public holidays and normal days.

        holiday_dates should contain dates in YYYY-MM-DD format.
        """

        data = dataframe.copy()

        data["transaction_datetime"] = pd.to_datetime(
            data["transaction_datetime"],
            errors="coerce"
        )

        data = data.dropna(
            subset=["transaction_datetime", "total_amount"]
        )

        data["date"] = (
            data["transaction_datetime"].dt.date
        )

        holiday_set = {
            pd.to_datetime(date).date()
            for date in holiday_dates
        }

        data["day_type"] = data["date"].apply(
            lambda date:
                "Public Holiday" if date in holiday_set
                else "Normal Day"
        )

        holiday_summary = (
            data.groupby("day_type")
            .agg(
                total_sales=("total_amount", "sum"),
                total_transactions=("transaction_id", "nunique")
            )
            .reset_index()
        )

        return holiday_summary
