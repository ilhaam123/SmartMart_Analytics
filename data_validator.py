
class DataValidator:
    """
    Responsible for validating SmartMart transaction data.
    """

    def validate_data(self, dataframe):
        """
        Checks the dataset for missing values,
        duplicate records and suspicious transaction values.
        """

        validation_results = {}

        # Check total missing values
        validation_results["missing_values"] = int(
            dataframe.isnull().sum().sum()
        )

        # Check duplicate records
        validation_results["duplicate_records"] = int(
            dataframe.duplicated().sum()
        )

        # Separate Sale and Return transactions
        sales = dataframe[
            dataframe["transaction_type"] == "Sale"
        ]

        returns = dataframe[
            dataframe["transaction_type"] == "Return"
        ]

        # Check invalid quantities in Sale transactions
        validation_results["invalid_quantities"] = int(
            (sales["quantity"] <= 0).sum()
        )

        # Check negative unit prices
        validation_results["invalid_prices"] = int(
            (dataframe["unit_price"] < 0).sum()
        )

        # Identify suspicious negative prices in Sale transactions
        validation_results["suspicious_sale_prices"] = int(
            (sales["unit_price"] < 0).sum()
        )

        # Check negative total amounts in Sale transactions
        validation_results["invalid_total_amounts"] = int(
            (sales["total_amount"] < 0).sum()
        )

        # Check invalid discount percentages
        validation_results["invalid_discounts"] = int(
            (
                (dataframe["discount_percent"] < 0) |
                (dataframe["discount_percent"] > 100)
            ).sum()
        )

        # Identify missing discount percentages
        validation_results["missing_discounts"] = int(
            dataframe["discount_percent"].isnull().sum()
        )

        # Check suspicious negative quantities in Return transactions
        validation_results["invalid_return_quantities"] = int(
            (returns["quantity"] >= 0).sum()
        )

        # Identify negative amounts in Return transactions
        # These are reported separately, not treated as errors.
        validation_results["return_transactions"] = int(
            len(returns)
        )

        # Check Sale transaction amount mismatches
        sales_with_discount = sales[
            sales["discount_percent"].notna()
        ].copy()

        expected_total = (
            sales_with_discount["quantity"] *
            sales_with_discount["unit_price"] *
            (
                1 -
                sales_with_discount["discount_percent"] / 100
            )
        )

        validation_results["mismatched_sale_amounts"] = int(
            (
                (
                    sales_with_discount["total_amount"]
                    - expected_total
                ).abs() > 0.02
            ).sum()
        )

        return validation_results
