import pandas as pd
import numpy as np
from split_owners import split_owners


df = pd.read_excel("Global-Nuclear-Power-Tracker-July-2024.xlsx", sheet_name="Data")

selected_columns = ['Owner', 'Capacity (MW)', 'Reactor Type', 'Status', 'Start Year', 'Retirement Year', 'Planned Retirement', 'Cancellation Year', 'Latitude', 'Longitude', 'Country/Area']
df = df[selected_columns]


df = split_owners(df)

# calculate and add 'Lifetime' column
#df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df['Country/Area'] = df['Country/Area'].str.lower()
df['Reactor Type'] = df['Reactor Type'].str.lower()
df = df.applymap(lambda x: "N/A" if pd.isna(x) or x=="nan" or x=="not found" else x)
#df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

df.to_excel('data_cleaned/nuclear_cleaned.xlsx', index=False)