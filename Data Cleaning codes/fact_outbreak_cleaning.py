import pandas as pd

# Load the outbreak dataset from your specific file path
df = pd.read_csv(r"C:\Users\MANOJ SAM\Downloads\fact outbreak cleaned.csv")

# Convert key metrics to numeric types to fix formatting issues
numeric_cols = [
    'containment_rate_pct', 'response_time_hours', 'alert_level',
    'predicted_cases', 'historical_cases', 'forecast_accuracy_pct',
    'hospital_readiness_score', 'resource_readiness_score'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing numerical values with their column medians
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Fill missing flag values with 0
flag_cols = ['new_outbreak_flag', 'controlled_flag', 'emergency_alert_flag']
for col in flag_cols:
    df[col] = df[col].fillna(0)

# Cap percentage columns at a maximum of 100%
pct_cols = ['containment_rate_pct', 'forecast_accuracy_pct']
for col in pct_cols:
    df[col] = df[col].clip(upper=100)

# Export the cleaned dataset back to your Downloads folder
df.to_csv(r"C:\Users\MANOJ SAM\Downloads\fact_outbreak_cleaned_output.csv", index=False)

print("Done! Cleaned shape:", df.shape)
