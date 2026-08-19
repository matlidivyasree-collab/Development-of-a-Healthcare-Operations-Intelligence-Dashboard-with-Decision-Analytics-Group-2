import pandas as pd

# ============================
# Load Dimension Tables
# ============================
dim_date=pd.read_csv("dim_state.csv")
dim_disease = pd.read_csv("dim_disease.csv")
dim_program = pd.read_csv("dim_program.csv")
dim_source = pd.read_csv("dim_source.csv")
dim_state = pd.read_csv("dim_state.csv")

fact_disease_surveillance = pd.read_csv("fact_disease_surveillance.csv")
fact_environmental = pd.read_csv("fact_environmental.csv")
fact_health_programs = pd.read_csv("fact_health_programs.csv")
fact_lab_healthcare = pd.read_csv("fact_lab_healthcare.csv")
fact_outbreak = pd.read_csv("fact_outbreak.csv")

# ============================
# Store all DataFrames in Dictionary
# ============================
tables = {
    "dim_date": dim_date,
    "dim_disease": dim_disease,
    "dim_program": dim_program,
    "dim_source": dim_source,
    "dim_state": dim_state,
    "fact_disease_surveillance": fact_disease_surveillance,
    "fact_environmental": fact_environmental,
    "fact_health_programs": fact_health_programs,
    "fact_lab_healthcare": fact_lab_healthcare,
    "fact_outbreak": fact_outbreak
}

# ============================
# Display Basic Information
# ============================
for table_name, df in tables.items():
    print("=" * 50)
    print(f"Table Name : {table_name}")
    print("=" * 50)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\n")

print("\n========== Missing Value Analysis ==========\n")

for table_name, df in tables.items():

    # Missing Values Count
    missing_count = df.isnull().sum()

    # Missing Percentage
    missing_percent = (missing_count / len(df)) * 100

    # Summary Table
    summary = pd.DataFrame({
        "Column Name": df.columns,
        "Missing Values": missing_count.values,
        "Missing Percentage": missing_percent.values.round(2)
    })

    print("="*60)
    print(f"Table : {table_name}")
    print("="*60)
    print(summary)
    print("\n")

print("\n========== Duplicate Records Analysis ==========\n")

for table_name, df in tables.items():

    # Count duplicate rows
    duplicate_count = df.duplicated().sum()

    # Duplicate percentage
    duplicate_percent = (duplicate_count / len(df)) * 100

    # Create summary
    summary = pd.DataFrame({
        "Table Name": [table_name],
        "Total Rows": [len(df)],
        "Duplicate Rows": [duplicate_count],
        "Duplicate Percentage": [round(duplicate_percent, 2)]
    })

    print(summary)
    print("-" * 70) 
print("\n========== Mismatched Keys Analysis ==========\n")

# Disease ID Check
invalid_disease = fact_disease_surveillance[
    ~fact_disease_surveillance["disease_id"].isin(dim_disease["disease_id"])
]
print("Invalid Disease IDs :", len(invalid_disease))

# State ID Check
invalid_state = fact_disease_surveillance[
    ~fact_disease_surveillance["state_id"].isin(dim_state["state_id"])
]
print("Invalid State IDs :", len(invalid_state))

# Source ID Check
invalid_source = fact_disease_surveillance[
    ~fact_disease_surveillance["source_id"].isin(dim_source["source_id"])
]
print("Invalid Source IDs :", len(invalid_source))

# Program ID Check
invalid_program = fact_health_programs[
    ~fact_health_programs["program_id"].isin(dim_program["program_id"])
]
print("Invalid Program IDs :", len(invalid_program))

# Date ID Check (Safe)
if "date_id" in dim_date.columns:
    invalid_date = fact_disease_surveillance[
        ~fact_disease_surveillance["date_id"].isin(dim_date["date_id"])
    ]
    print("Invalid Date IDs :", len(invalid_date))
else:
    print("date_id column not found in dim_date table")
    print("Available columns are:")
    print(dim_date.columns.tolist())
print("\n========== Invalid Categories ==========\n")

print("Hotspot Flag Values:")
print(fact_environmental["hotspot_flag"].unique())

print("\nNew Outbreak Flag Values:")
print(fact_outbreak["new_outbreak_flag"].unique())

print("\nControlled Flag Values:")
print(fact_outbreak["controlled_flag"].unique())

print("\nEmergency Alert Flag Values:")
print(fact_outbreak["emergency_alert_flag"].unique())
yes_values = ["YES", "Yes", "yes", "Y", "True", "TRUE", "1"]
no_values = ["NO", "No", "no", "N", "False", "FALSE", "0"]

fact_environmental["hotspot_flag"] = fact_environmental["hotspot_flag"].replace(yes_values, "YES")
fact_environmental["hotspot_flag"] = fact_environmental["hotspot_flag"].replace(no_values, "NO")

fact_outbreak["new_outbreak_flag"] = fact_outbreak["new_outbreak_flag"].replace(yes_values, "YES")

fact_outbreak["controlled_flag"] = fact_outbreak["controlled_flag"].replace(yes_values, "YES")
fact_outbreak["controlled_flag"] = fact_outbreak["controlled_flag"].replace(no_values, "NO")

fact_outbreak["emergency_alert_flag"] = fact_outbreak["emergency_alert_flag"].replace(yes_values, "YES")
fact_outbreak["emergency_alert_flag"] = fact_outbreak["emergency_alert_flag"].replace(no_values, "NO")  

print("\n========== Date Format & Date Range Analysis ==========\n")

# Convert to datetime
fact_disease_surveillance["report_date"] = pd.to_datetime(
    fact_disease_surveillance["report_date_raw"],
    errors="coerce",
    format="mixed"
)

# Invalid dates
invalid_dates = fact_disease_surveillance["report_date"].isnull().sum()
print("Invalid Date Values :", invalid_dates)

# Future dates
future_dates = fact_disease_surveillance[
    fact_disease_surveillance["report_date"] > pd.Timestamp.today()
]

print("Future Dates :", len(future_dates))

# Minimum & Maximum Date
print("Minimum Date :", fact_disease_surveillance["report_date"].min())
print("Maximum Date :", fact_disease_surveillance["report_date"].max())  
import matplotlib.pyplot as plt
import seaborn as sns

# Example: fact_disease_surveillance table
plt.figure(figsize=(12,6))

sns.heatmap(
    fact_disease_surveillance.isnull(),
    cbar=False,
    cmap="viridis",
    yticklabels=False
)

plt.title("Missing Value Heatmap - fact_disease_surveillance")
plt.xlabel("Columns")
plt.ylabel("Rows")

plt.savefig("missing_heatmap.png")
plt.close()

print("\n========== Data Quality Summary ==========\n")

summary_data = []

for table_name, df in tables.items():

    total_rows = len(df)
    total_columns = len(df.columns)

    # Total Missing Values
    missing_values = df.isnull().sum().sum()

    # Missing Percentage
    missing_percentage = round((missing_values / (total_rows * total_columns)) * 100, 2)

    # Duplicate Rows
    duplicate_rows = df.duplicated().sum()

    # Duplicate Percentage
    duplicate_percentage = round((duplicate_rows / total_rows) * 100, 2)

    summary_data.append({
        "Table Name": table_name,
        "Rows": total_rows,
        "Columns": total_columns,
        "Missing Values": missing_values,
        "Missing %": missing_percentage,
        "Duplicate Rows": duplicate_rows,
        "Duplicate %": duplicate_percentage
    })

# Create Summary DataFrame
summary_df = pd.DataFrame(summary_data)

# Display Output
print(summary_df)
summary_df.to_csv("data_quality_summary.csv", index=False)

print("Summary CSV Saved Successfully")
