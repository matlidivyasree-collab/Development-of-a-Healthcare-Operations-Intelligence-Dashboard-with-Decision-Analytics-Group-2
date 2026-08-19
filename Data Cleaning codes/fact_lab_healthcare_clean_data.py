import pandas as pd

df = pd.read_csv(r"C:\Users\srava\Downloads\fact_lab_healthcare.csv")

df["total_tests"] = pd.to_numeric(df["total_tests"], errors="coerce")

df = df.drop_duplicates()

df["total_tests"] = df["total_tests"].fillna(df["total_tests"].median())
df["positive_tests"] = df["positive_tests"].fillna(df["positive_tests"].median())
df["vaccination_coverage_pct"] = df["vaccination_coverage_pct"].fillna(df["vaccination_coverage_pct"].median())
df["hospital_beds"] = df["hospital_beds"].fillna(df["hospital_beds"].median())
df["reporting_compliance_pct"] = df["reporting_compliance_pct"].fillna(df["reporting_compliance_pct"].median())

df["doctors"] = df["doctors"].abs()

df["icu_utilization_pct"] = df["icu_utilization_pct"].clip(upper=100)
df["bed_occupancy_pct"] = df["bed_occupancy_pct"].clip(upper=100)

df.to_csv(r"C:\Users\srava\Downloads\fact_lab_healthcare_cleaned.csv", index=False)

print("Done! Shape:", df.shape)
