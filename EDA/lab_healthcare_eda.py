import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

#Load Dataset
df = pd.read_csv('fact_lab_healthcare_cleaned.csv')

#Dataset Summary & Missing Value Audit
print("=== DATASET OVERVIEW ===")
print(f"Total Rows: {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}")
print("\nMissing Values Count:")
print(df.isnull().sum())

#Generate Descriptive Statistics
eda_summary = df.describe().T
eda_summary['missing_values'] = df.isnull().sum()
eda_summary['data_type'] = df.dtypes

# Export Summary CSV
eda_summary.to_csv('EDA_Output(Business Insights).csv')
print("\n[SUCCESS] 'EDA_Output(Business Insights).csv' generated.")

# 4. State-Level Aggregations
state_insights = (
    df.groupby('state_id')
    .agg(
        total_tests=('total_tests', 'sum'),
        total_positive=('positive_tests', 'sum'),
        avg_positivity=('positivity_rate', 'mean'),
        avg_icu_utilization=('icu_utilization_pct', 'mean'),
        avg_turnaround_days=('turnaround_time_days', 'mean'),
        avg_compliance=('reporting_compliance_pct', 'mean'),
    )
    .reset_index()
)

print("\n=== TOP 5 STATES BY TEST VOLUME ===")
print(state_insights.sort_values(by='total_tests', ascending=False).head())

#Visualizations
sns.set_theme(style='whitegrid')

# Fig1: Distributions
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.histplot(df['positivity_rate'], kde=True, ax=axes[0, 0], color='skyblue')
axes[0, 0].set_title('Test Positivity Rate (%)')

sns.histplot(df['bed_occupancy_pct'], kde=True, ax=axes[0, 1], color='salmon')
axes[0, 1].set_title('Bed Occupancy Rate (%)')

sns.histplot(
    df['icu_utilization_pct'], kde=True, ax=axes[1, 0], color='purple'
)
axes[1, 0].set_title('ICU Utilization Rate (%)')

sns.histplot(
    df['turnaround_time_days'], kde=True, ax=axes[1, 1], color='teal'
)
axes[1, 1].set_title('Lab Turnaround Time (Days)')

plt.tight_layout()
plt.savefig('distribution_plots.png', dpi=300)
plt.close()

# Fig2: Correlation Heatmap
plt.figure(figsize=(10, 8))
corr_cols = [
    'total_tests',
    'positive_tests',
    'positivity_rate',
    'hospital_beds',
    'doctors',
    'icu_utilization_pct',
    'turnaround_time_days',
]
sns.heatmap(df[corr_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Healthcare Metrics Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300)
plt.close()

print("[SUCCESS] All analysis and plots completed.")