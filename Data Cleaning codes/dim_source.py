import pandas as pd

df = pd.read_csv(r"C:\Users\lucky\OneDrive\Documents\dim_source.csv")

print("First 5 Rows:")
print(df.head())

print("\nLast 5 Rows:")
print(df.tail())

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nInfo:")
print(df.info())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

df = df.drop_duplicates()

df["source_name"] = df["source_name"].str.strip()

df["source_name"] = df["source_name"].str.title()

print("\nDuplicate Source IDs:")
print(df["source_id"].duplicated().sum())

print("\nDuplicate Source Names:")
print(df["source_name"].duplicated().sum())

print("\nUnique Source Names:")
print(df["source_name"].unique())

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Shape:")
print(df.shape)

print("\nCleaned Dataset:")
print(df)

df.to_excel("Cleaned_Source_Master.xlsx", index=False)
