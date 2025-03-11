import pandas as pd
import numpy as np
from split_owners import split_owners


df_data = pd.read_excel("Global-Oil-and-Gas-Plant-Tracker-GOGPT-January-2025.xlsx", sheet_name="Gas & Oil Units")
df_threshold = pd.read_excel("Global-Oil-and-Gas-Plant-Tracker-GOGPT-January-2025.xlsx", sheet_name="sub-threshold units")

df = pd.concat([df_data, df_threshold], ignore_index=True)

selected_columns = ['Owner(s)', 'Fuel', 'Capacity (MW)', 'Turbine/Engine Technology', 'Status', 'Start year', 'Retired year', 'Planned retire', 'Latitude', 'Longitude', 'Country/Area']
df = df[selected_columns]
df = df.rename(columns={"Owner(s)": "Owner"})

 
df = split_owners(df)

# calculate and add 'Lifetime' column
#df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df['Country/Area'] = df['Country/Area'].str.lower()
df['Fuel'] = df['Fuel'].str.lower()
df = df.applymap(lambda x: "N/A" if pd.isna(x) or x=="nan" or x=="not found" else x)
#df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

df.to_excel('data_cleaned/oil_gas_cleaned.xlsx', index=False)