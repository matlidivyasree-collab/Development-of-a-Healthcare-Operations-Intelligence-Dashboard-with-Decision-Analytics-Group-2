import pandas as pd
df=pd.read_csv("phs_dataset/dim_program.csv")
print("Read the datasuccesfully.")
print(df)
#Check the information :
print(df.info())
#Check the data type:
print(df.dtypes)
#Check for null value:
print(df.isnull().sum())
#Check for duplicate
print("Dupliated present or not:")
print(df.duplicated().sum())
#Remove completely empty rows
df = df.dropna(how="all")   
#Remove extra spaces from column names    
df.columns = df.columns.str.strip()
# Save the cleaned dataset
df.to_csv("Clean_data_set/dim_program_clean.csv", index=False)

print("Cleaned dataset saved successfully as 'dim_program_clean.csv'.")