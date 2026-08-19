import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
sns.set_style("whitegrid")

df = pd.read_csv("fact_lab_healthcare_cleaned.csv")

print(df.head())
print(df.tail())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe())

print(df.isnull().sum())
print(df.duplicated().sum())
print(df.dtypes)

print("\nAverage Vaccination Coverage:")
print(df["vaccination_coverage_pct"].mean())

print("\nMedian Vaccination Coverage:")
print(df["vaccination_coverage_pct"].median())

print("\nMaximum Vaccination Coverage:")
print(df["vaccination_coverage_pct"].max())

print("\nMinimum Vaccination Coverage:")
print(df["vaccination_coverage_pct"].min())

state_vaccination = df.groupby("state_id")[
    "vaccination_coverage_pct"
].mean()

print("\nVaccination Coverage by State:")
print(state_vaccination)



target = 90

lagging_states = state_vaccination[
    state_vaccination < target
]

print("\nStates Below 90% Vaccination Target:")
print(lagging_states)



plt.figure(figsize=(10, 8))

state_vaccination.sort_values().plot(
    kind="barh"
)

plt.axvline(
    target,
    linestyle="--",
    label="90% Target"
)

plt.title("Vaccination Coverage by State")
plt.xlabel("Vaccination Coverage (%)")
plt.ylabel("State")
plt.legend()

plt.show()



average = df["vaccination_coverage_pct"].mean()

plt.figure(figsize=(8, 4))

plt.barh(
    ["Vaccination Coverage"],
    [average]
)

plt.xlim(0, 100)

plt.axvline(
    target,
    linestyle="--",
    label="90% Target"
)

plt.xlabel("Percentage")
plt.title("Overall Vaccination Coverage")

plt.legend()
plt.show()



plt.figure(figsize=(7, 5))

sns.scatterplot(
    data=df,
    x="vaccination_coverage_pct",
    y="positivity_rate"
)

plt.title("Vaccination Coverage vs Positivity Rate")
plt.xlabel("Vaccination Coverage (%)")
plt.ylabel("Positivity Rate (%)")

plt.show()


plt.figure(figsize=(7, 5))

sns.scatterplot(
    data=df,
    x="vaccination_coverage_pct",
    y="icu_utilization_pct"
)

plt.title("Vaccination Coverage vs ICU Utilization")
plt.xlabel("Vaccination Coverage (%)")
plt.ylabel("ICU Utilization (%)")

plt.show()
# ---------------------------------------------------------
# TOP AND BOTTOM STATES
# ---------------------------------------------------------

print("\nTop 5 States:")
print(state_vaccination.sort_values(ascending=False).head())

print("\nBottom 5 States:")
print(state_vaccination.sort_values().head())

# ---------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------

print("\nMean:")
print(df.mean(numeric_only=True))

print("\nMedian:")
print(df.median(numeric_only=True))

print("\nMaximum:")
print(df.max(numeric_only=True))

print("\nMinimum:")
print(df.min(numeric_only=True))

print("\nStandard Deviation:")
print(df.std(numeric_only=True))

# ---------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------

df.to_csv("Vaccination_EDA_Output1.csv", index=False)

print("\nEDA Completed Successfully")