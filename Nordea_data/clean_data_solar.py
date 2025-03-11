import pandas as pd
from split_owners import split_owners

df_data = pd.read_excel("Global-Solar-Power-Tracker-February-2025.xlsx", sheet_name="20 MW+")
df_threshold = pd.read_excel("Global-Solar-Power-Tracker-February-2025.xlsx", sheet_name="1-20 MW")

df = pd.concat([df_data, df_threshold], ignore_index=True)

selected_columns = ['Owner', 'Capacity (MW)', 'Technology Type', 'Status', 'Start year', 'Retired year', 'Latitude', 'Longitude', 'Country/Area']
df = df[selected_columns]
df = split_owners(df)

# calculate and add 'Lifetime' column
# df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df['Country/Area'] = df['Country/Area'].str.lower()
df['Technology Type'] = df['Technology Type'].str.lower()

df = df.applymap(lambda x: "N/A" if pd.isna(x) else x)
# df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

df.to_excel('data_cleaned/solar_cleaned.xlsx', index=False)