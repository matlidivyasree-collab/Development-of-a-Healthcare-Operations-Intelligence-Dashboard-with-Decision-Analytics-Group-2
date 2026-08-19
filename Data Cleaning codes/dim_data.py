import pandas as pd

df = pd.read_csv("dim_date.csv")

print(df.head())

print(df.info())

print(df.isnull().sum())

df = df.drop_duplicates()

df["full_date"] = pd.to_datetime(df["full_date"])

df["month_name"] = df["month_name"].str.strip()

df["quarter"] = df["quarter"].str.strip()

print(df.dtypes)

print(df.shape)

df.to_csv("cleaned_dates.csv", index=False)

print("Data cleaned successfully!")