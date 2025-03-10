import pandas as pd

# load data
df_data = pd.read_excel("Global-Wind-Power-Tracker-February-2025.xlsx", sheet_name="Data")
df_threshold = pd.read_excel("Global-Wind-Power-Tracker-February-2025.xlsx", sheet_name="Below Threshold")

# merge above and below threshold data
df = df_data.append(df_threshold)

# extract needed columns and create new dataframe
selected_columns = ['Country/Area', 'Capacity (MW)', 'Installation Type', 'Status', 'Start year', 'Retired year', 'Owner', 'Latitude', 'Longitude']
df = df[selected_columns]

# calculate and add 'Lifetime' column
df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df = df.applymap(lambda x: "N/A" if pd.isna(x) or x == '' else x)
df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

# write dataframe to excel file
df.to_excel('wind_cleaned.xlsx', index=False)
