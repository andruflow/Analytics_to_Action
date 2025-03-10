import pandas as pd
import numpy as np

df_data = pd.read_excel("Global-Wind-Power-Tracker-February-2025.xlsx", sheet_name="Data")
df_threshold = pd.read_excel("Global-Wind-Power-Tracker-February-2025.xlsx", sheet_name="Below Threshold")

df = df_data.append(df_threshold)

selected_columns = ['Country/Area', 'Capacity (MW)', 'Installation Type', 'Start year', 'Retired year', 'Owner', 'Latitude', 'Longitude']
df = df[selected_columns]
df["Owner"] = df["Owner"].apply(lambda x: "N/A" if pd.isna(x) else x)
df["Start year"] = df["Start year"].apply(lambda x: "N/A" if pd.isna(x) else x)
df["Retired year"] = df["Retired year"].apply(lambda x: "N/A" if pd.isna(x) else x)

df.to_excel('wind_cleaned.xlsx', index=False)