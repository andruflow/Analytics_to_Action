import pandas as pd

df_data = pd.read_excel("Global-Solar-Power-Tracker-February-2025.xlsx", sheet_name="20 MW+")
df_threshold = pd.read_excel("Global-Solar-Power-Tracker-February-2025.xlsx", sheet_name="1-20 MW")

df = df_data.append(df_threshold)

selected_columns = ['Country/Area', 'Capacity (MW)', 'Technology Type', 'Status', 'Start year', 'Retired year', 'Owner', 'Latitude', 'Longitude']
df = df[selected_columns]

# calculate and add 'Lifetime' column
df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df = df.applymap(lambda x: "N/A" if pd.isna(x) else x)
df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

df.to_excel('solar_cleaned.xlsx', index=False)
