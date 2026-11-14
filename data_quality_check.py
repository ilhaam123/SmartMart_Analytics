from data_reader import ExcelDataReader
from data_validator import DataValidator


# Read the SmartMart dataset
reader = ExcelDataReader()

dataframe = reader.read_data(
    "data/smartretail_transactions.xlsx"
)

# Validate the dataset
validator = DataValidator()

results = validator.validate_data(dataframe)

# Display dataset information
print("\n===== SMARTMART DATA QUALITY REPORT =====")

print("Total Records:", len(dataframe))
print("Total Columns:", len(dataframe.columns))

print("\n===== VALIDATION RESULTS =====")

for issue, count in results.items():
    print(f"{issue.replace('_', ' ').title()}: {count}")

print("\n===== MISSING VALUES BY COLUMN =====")

missing_values = dataframe.isnull().sum()

print(missing_values[missing_values > 0])

print("\n===== END OF REPORT =====")
