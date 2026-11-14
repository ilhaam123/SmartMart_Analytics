from data_reader import ExcelDataReader

# Read the SmartMart dataset
reader = ExcelDataReader()

file_path = "data/smartretail_transactions.xlsx"

dataframe = reader.read_data(file_path)


# ==========================================
# 1. TRANSACTION TYPE INVESTIGATION
# ==========================================

print("\n===== TRANSACTION TYPES =====")

print(dataframe["transaction_type"].value_counts())


# ==========================================
# 2. QUANTITY ANALYSIS
# ==========================================

print("\n===== QUANTITY ANALYSIS =====")

print(
    "Negative quantities:",
    (dataframe["quantity"] < 0).sum()
)

print(
    "Zero quantities:",
    (dataframe["quantity"] == 0).sum()
)


# ==========================================
# 3. PRICE ANALYSIS
# ==========================================

print("\n===== PRICE ANALYSIS =====")

print(
    "Negative unit prices:",
    (dataframe["unit_price"] < 0).sum()
)


# ==========================================
# 4. NEGATIVE AMOUNT EXAMPLES
# ==========================================

print("\n===== NEGATIVE AMOUNT EXAMPLES =====")

negative_amounts = dataframe[
    dataframe["total_amount"] < 0
]

print(
    negative_amounts[
        [
            "transaction_type",
            "quantity",
            "unit_price",
            "total_amount"
        ]
    ].head(10)
)


# ==========================================
# 5. NEGATIVE UNIT PRICE INVESTIGATION
# ==========================================

print("\n===== NEGATIVE UNIT PRICE INVESTIGATION =====")

negative_prices = dataframe[
    dataframe["unit_price"] < 0
]

print(
    "Total negative unit price records:",
    len(negative_prices)
)

print("\nTransaction types:")

print(
    negative_prices["transaction_type"].value_counts()
)

print("\nExamples:")

print(
    negative_prices[
        [
            "transaction_type",
            "quantity",
            "unit_price",
            "discount_percent",
            "total_amount"
        ]
    ].head(15)
)


# ==========================================
# 6. SALES AMOUNT VALIDATION
# ==========================================

print("\n===== SALES AMOUNT VALIDATION =====")

# Select Sale transactions
sales = dataframe[
    dataframe["transaction_type"] == "Sale"
].copy()

# Calculate expected total amount
sales["expected_total"] = (
    sales["quantity"]
    * sales["unit_price"]
    * (1 - sales["discount_percent"] / 100)
)

# Identify mismatches only when discount is available
mismatches = sales[
    (
        sales["discount_percent"].notna()
    ) &
    (
        abs(
            sales["total_amount"] -
            sales["expected_total"]
        ) > 0.02
    )
]

print("Total sale records:", len(sales))

print(
    "Records with mismatched amounts:",
    len(mismatches)
)

print("\nExamples:")

print(
    mismatches[
        [
            "quantity",
            "unit_price",
            "discount_percent",
            "total_amount",
            "expected_total"
        ]
    ].head(10)
)


# ==========================================
# 7. DETAILED SALES MISMATCH ANALYSIS
# ==========================================

print("\n===== DETAILED SALES MISMATCH ANALYSIS =====")

positive_price_sales = sales[
    sales["unit_price"] > 0
]

negative_price_sales = sales[
    sales["unit_price"] < 0
]

positive_price_mismatches = mismatches[
    mismatches["unit_price"] > 0
]

negative_price_mismatches = mismatches[
    mismatches["unit_price"] < 0
]

print(
    "Sales with positive prices:",
    len(positive_price_sales)
)

print(
    "Mismatches among positive-price sales:",
    len(positive_price_mismatches)
)

print(
    "Sales with negative prices:",
    len(negative_price_sales)
)

print(
    "Mismatches among negative-price sales:",
    len(negative_price_mismatches)
)

print(
    "Sales with missing discounts:",
    sales["discount_percent"].isnull().sum()
)


# ==========================================
# 8. FINAL MISMATCH COUNTS
# ==========================================

print("\n===== FINAL MISMATCH COUNTS =====")

print(
    "Mismatches excluding missing discounts:",
    len(mismatches)
)

print(
    "Positive-price mismatches:",
    len(positive_price_mismatches)
)

print(
    "Negative-price mismatches:",
    len(negative_price_mismatches)
)

print("\n===== INVESTIGATION COMPLETED =====")
# ==========================================
# 9. POSITIVE-PRICE SALES MISMATCH ANALYSIS
# ==========================================

print("\n===== POSITIVE-PRICE MISMATCH ANALYSIS =====")

# Select positive-price sales with mismatched amounts
positive_mismatches = mismatches[
    mismatches["unit_price"] > 0
].copy()

# Calculate the difference between actual and expected amounts
positive_mismatches["amount_difference"] = (
    positive_mismatches["total_amount"]
    - positive_mismatches["expected_total"]
)

print(
    "Total positive-price mismatches:",
    len(positive_mismatches)
)

print(
    "\nAverage amount difference:",
    round(
        positive_mismatches["amount_difference"].mean(),
        2
    )
)

print(
    "Largest positive difference:",
    round(
        positive_mismatches["amount_difference"].max(),
        2
    )
)

print(
    "Largest negative difference:",
    round(
        positive_mismatches["amount_difference"].min(),
        2
    )
)

print("\nFirst 10 mismatch examples:")

print(
    positive_mismatches[
        [
            "quantity",
            "unit_price",
            "discount_percent",
            "total_amount",
            "expected_total",
            "amount_difference"
        ]
    ].head(10)
)
# ==========================================
# 10. EXTREME UNIT PRICE INVESTIGATION
# ==========================================

print("\n===== EXTREME UNIT PRICE INVESTIGATION =====")

positive_sales = sales[
    sales["unit_price"] > 0
]

print("\nHighest 10 unit prices:")

print(
    positive_sales[
        [
            "product_name",
            "quantity",
            "unit_price",
            "discount_percent",
            "total_amount"
        ]
    ]
    .sort_values(
        by="unit_price",
        ascending=False
    )
    .head(10)
)

print("\nUnit price statistics:")

print(
    positive_sales["unit_price"].describe()
)
import pandas as pd

df = pd.read_excel("data/smartretail_transactions.xlsx")

print("Original Region Values:")
print(df["region"].value_counts(dropna=False))

print("\nStandardised Region Values:")
print(df["region"].str.strip().str.title().value_counts(dropna=False))