import pandas as pd
import numpy as np
from split_owners import split_owners


df_data = pd.read_excel("Global-Hydropower-Tracker-April-2024.xlsx", sheet_name="Data")
df_threshold = pd.read_excel("Global-Hydropower-Tracker-April-2024.xlsx", sheet_name="Below Threshold")

# merge above and below threshold data
df = pd.concat([df_data, df_threshold], ignore_index=True)

selected_columns = ['Owner', 'Capacity (MW)', 'Technology Type', 'Status', 'Start Year', 'Retired Year', 'Latitude', 'Longitude', 'Country 1']
df = df[selected_columns]


df = split_owners(df)

# calculate and add 'Lifetime' column
#df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df['Country 1'] = df['Country 1'].str.lower()
df = df.applymap(lambda x: "N/A" if pd.isna(x) or x=="nan" or x=="not found" else x)
#df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

df.to_excel('data_cleaned/hydro_cleaned.xlsx', index=False)