import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("fact_disease_surveillance_cleaned.csv")

print(df.head())

print(df.columns)

print(df[[
    "total_reported_cases",
    "deaths",
    "recovery_rate",
    "public_health_risk_score"
]].head(10))

Q1 = df["total_reported_cases"].quantile(0.25)
Q3 = df["total_reported_cases"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Limit:", lower_limit)
print("Upper Limit:", upper_limit)

outliers = df[df["total_reported_cases"] > upper_limit]

print("Number of outliers:", len(outliers))
print(outliers[["fact_id", "total_reported_cases"]])

Q1_deaths = df["deaths"].quantile(0.25)
Q3_deaths = df["deaths"].quantile(0.75)

IQR_deaths = Q3_deaths - Q1_deaths

lower_deaths = Q1_deaths - 1.5 * IQR_deaths
upper_deaths = Q3_deaths + 1.5 * IQR_deaths

print("Deaths Lower Limit:", lower_deaths)
print("Deaths Upper Limit:", upper_deaths)

death_outliers = df[df["deaths"] > upper_deaths]

print("Number of death outliers:", len(death_outliers))

Q1_recovery = df["recovery_rate"].quantile(0.25)
Q3_recovery = df["recovery_rate"].quantile(0.75)

IQR_recovery = Q3_recovery - Q1_recovery

lower_recovery = Q1_recovery - 1.5 * IQR_recovery
upper_recovery = Q3_recovery + 1.5 * IQR_recovery

print("Recovery Lower Limit:", lower_recovery)
print("Recovery Upper Limit:", upper_recovery)

recovery_outliers = df[
    (df["recovery_rate"] < lower_recovery) |
    (df["recovery_rate"] > upper_recovery)
]

print("Number of recovery outliers:", len(recovery_outliers))

Q1_risk = df["public_health_risk_score"].quantile(0.25)
Q3_risk = df["public_health_risk_score"].quantile(0.75)

IQR_risk = Q3_risk - Q1_risk

lower_risk = Q1_risk - 1.5 * IQR_risk
upper_risk = Q3_risk + 1.5 * IQR_risk

print("Risk Score Lower Limit:", lower_risk)
print("Risk Score Upper Limit:", upper_risk)

risk_outliers = df[
    (df["public_health_risk_score"] < lower_risk) |
    (df["public_health_risk_score"] > upper_risk)
]

print("Number of risk score outliers:", len(risk_outliers))

columns = [
    "total_reported_cases",
    "deaths",
    "recovery_rate",
    "public_health_risk_score"
]

for col in columns:
    mean = df[col].mean()
    std = df[col].std()

    z_score = (df[col] - mean) / std

    outliers = df[z_score.abs() > 3]

    print(col, "Z-score outliers:", len(outliers))

    print("----- IQR vs Z-score Comparison -----")

print("Total Reported Cases: IQR = 962, Z-score = 281")
print("Deaths: IQR = 1314, Z-score = 275")
print("Recovery Rate: IQR = 136, Z-score = 136")
print("Risk Score: IQR = 457, Z-score = 192")

plt.boxplot(df["total_reported_cases"])
plt.title("Boxplot - Total Reported Cases")
plt.ylabel("Total Reported Cases")
plt.show()

plt.boxplot(df["deaths"])
plt.title("Boxplot - Deaths")
plt.ylabel("Deaths")
plt.show()

plt.boxplot(df["recovery_rate"])
plt.title("Boxplot - Recovery Rate")
plt.ylabel("Recovery Rate")
plt.show()

plt.boxplot(df["public_health_risk_score"])
plt.title("Boxplot - Public Health Risk Score")
plt.ylabel("Risk Score")
plt.show()

z = (df["total_reported_cases"] - df["total_reported_cases"].mean()) / df["total_reported_cases"].std()

plt.scatter(df.index, z)
plt.axhline(3)
plt.axhline(-3)
plt.title("Z-score Scatter Plot - Total Reported Cases")
plt.xlabel("Record")
plt.ylabel("Z-score")
plt.show()