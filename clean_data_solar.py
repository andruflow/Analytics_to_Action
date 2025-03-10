import pandas as pd
import numpy as np

df_data = pd.read_excel("Global-Solar-Power-Tracker-February-2025.xlsx", sheet_name="20 MW+")
df_threshold = pd.read_excel("Global-Solar-Power-Tracker-February-2025.xlsx", sheet_name="1-20 MW")

df = df_data.append(df_threshold)

selected_columns = ['Country/Area', 'Capacity (MW)', 'Technology Type', 'Start year', 'Retired year', 'Owner', 'Latitude', 'Longitude']
df = df[selected_columns]
df = df.applymap(lambda x: "N/A" if pd.isna(x) else x)

df.to_excel('solar_cleaned.xlsx', index=False)