import pandas as pd
from split_owners import split_owners
from owners_function import process_owners

# load data
df_data = pd.read_excel("Global-Bioenergy-Power-Tracker-GBPT-September-2024.xlsx", sheet_name="Data")
df_threshold = pd.read_excel("Global-Bioenergy-Power-Tracker-GBPT-September-2024.xlsx", sheet_name="Below Threshold")

# merge above and below threshold data
df = pd.concat([df_data, df_threshold], ignore_index=True)

# extract needed columns and create new dataframe
selected_columns = ['Owner(s)', 'Capacity (MW)', 'Fuel', 'Status', 'Start Year', 'Retired Year', 'Latitude', 'Longitude', 'Country/Area']
df = df[selected_columns]
df = df.rename(columns={"Owner(s)": "Owner"})

df = split_owners(df)


# calculate and add 'Lifetime' column
# df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df['Country/Area'] = df['Country/Area'].str.lower()
df['Fuel'] = df['Fuel'].str.lower()
df = df.applymap(lambda x: "N/A" if pd.isna(x) or x == '' else x)
# df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

# write dataframe to excel file
df.to_excel('data_cleaned/bio_cleaned.xlsx', index=False)



