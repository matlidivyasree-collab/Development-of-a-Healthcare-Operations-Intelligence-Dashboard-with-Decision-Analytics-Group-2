import pandas as pd

# Load the CSV file
df = pd.read_csv("dim_disease.csv")

# Remove leading and trailing spaces from all string columns
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

# Remove "(Screening)" from disease names
df["disease_name"] = df["disease_name"].str.replace(
    r"\s*\(Screening\)", "", regex=True
)

# Remove duplicate rows (if any)
df = df.drop_duplicates()

# Remove rows with missing values (if any)
df = df.dropna()

# Ensure disease_id is integer
df["disease_id"] = df["disease_id"].astype(int)

# Save the cleaned data
df.to_csv("cleaned_disease.csv", index=False)

# Display cleaned data
print(df)