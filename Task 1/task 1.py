import pandas as pd

# Load dataset
df = pd.read_csv("marketing_campaign.csv", sep=";")  # This dataset uses semicolon separator
print(df.head())
print(df.info())
print(df.describe())
# Show missing values
print(df.isnull().sum())

# Drop rows with missing values (or use imputation depending on case)
df.dropna(inplace=True)
# Remove exact duplicate rows
df.drop_duplicates(inplace=True)
# Standardize text in categorical columns
df['Education'] = df['Education'].str.strip().str.lower()
df['Marital_Status'] = df['Marital_Status'].str.strip().str.lower()
# Convert Dt_Customer to datetime
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
# Ensure numerical columns are of correct type
df['Income'] = pd.to_numeric(df['Income'], errors='coerce')
df['Year_Birth'] = df['Year_Birth'].astype(int)
# Clean column names (lowercase, replace spaces with underscores)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
# Save to new CSV file
df.to_csv("cleaned_marketing_campaign.csv", index=False)
