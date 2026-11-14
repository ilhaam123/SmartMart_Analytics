
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CustomerAnalyzer:
    """
    Performs customer behaviour and segmentation analysis.
    """

    def get_customer_frequency(self, dataframe):
        """
        Categorises customers based on the number of Sale transactions.
        One-time: 1 transaction
        Occasional: 2-5 transactions
        Frequent: 6 or more transactions.
        """

        sales = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        customer_counts = (
            sales.dropna(subset=["customer_id"])
            .groupby("customer_id")["transaction_id"]
            .nunique()
        )

        categories = customer_counts.apply(
            lambda count:
                "One-time" if count == 1
                else "Occasional" if count <= 5
                else "Frequent"
        )

        frequency_summary = (
            categories.value_counts()
            .reindex(
                ["One-time", "Occasional", "Frequent"],
                fill_value=0
            )
        )

        return frequency_summary

    def get_customer_clusters(self, dataframe, number_of_clusters=3):
        """
        Groups customers using K-means based on:
        - Purchase frequency
        - Average basket value
        """

        sales = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        sales = sales.dropna(
            subset=["customer_id", "transaction_id", "total_amount"]
        )

        customer_data = sales.groupby("customer_id").agg(
            purchase_frequency=("transaction_id", "nunique"),
            average_basket_value=("total_amount", "mean")
        ).reset_index()

        customer_data = customer_data[
            (customer_data["purchase_frequency"] > 0) &
            (customer_data["average_basket_value"] > 0)
        ]

        if len(customer_data) < number_of_clusters:
            return pd.DataFrame()

        features = customer_data[
            ["purchase_frequency", "average_basket_value"]
        ]

        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        kmeans = KMeans(
            n_clusters=number_of_clusters,
            random_state=42,
            n_init=10
        )

        customer_data["cluster"] = kmeans.fit_predict(
            scaled_features
        )

        return customer_data

    def get_customer_age_groups(self, dataframe):
        """
        Summarises Sale transactions by customer age group.
        """

        sales = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        sales = sales.dropna(
            subset=["customer_id", "customer_age"]
        )

        sales["age_group"] = pd.cut(
            sales["customer_age"],
            bins=[0, 25, 35, 45, 55, float("inf")],
            labels=[
                "18-25", "26-35", "36-45",
                "46-55", "56+"
            ]
        )

        age_summary = (
            sales.dropna(subset=["age_group"])
            .groupby("age_group", observed=False)
            .agg(
                customers=("customer_id", "nunique"),
                transactions=("transaction_id", "nunique"),
                sales_amount=("total_amount", "sum")
            )
            .reset_index()
        )

        return age_summary

    def get_top_customer_cities(self, dataframe, limit=10):
        """
        Finds the top customer cities based on Sale revenue.
        """

        sales = dataframe[
            dataframe["transaction_type"] == "Sale"
        ].copy()

        sales = sales.dropna(
            subset=["customer_city", "total_amount"]
        )

        city_summary = (
            sales.groupby("customer_city")
            .agg(
                total_sales=("total_amount", "sum"),
                total_transactions=("transaction_id", "nunique")
            )
            .sort_values("total_sales", ascending=False)
            .head(limit)
            .reset_index()
        )

        return city_summary
