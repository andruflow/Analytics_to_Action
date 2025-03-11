import pandas as pd
from split_owners import split_owners
from owners_function import process_owners

# load data
df_data = pd.read_excel("Geothermal-Power-Tracker-May-2024.xlsx", sheet_name="Data")
df_threshold = pd.read_excel("Geothermal-Power-Tracker-May-2024.xlsx", sheet_name="Below Threshold")

# merge above and below threshold data
df = pd.concat([df_data, df_threshold], ignore_index=True)

# extract needed columns and create new dataframe
selected_columns = ['Owner', 'Capacity (MW)', 'Technology', 'Status', 'Start year', 'Retired year', 'Latitude', 'Longitude', 'Country/Area']
df = df[selected_columns]

df = split_owners(df)


# calculate and add 'Lifetime' column
# df['Lifetime'] = pd.to_numeric(df['Retired year'], errors='coerce') - pd.to_numeric(df['Start year'], errors='coerce')

# turn 'Owner' into lower case and replace empty tiles with 'N/A'
df['Owner'] = df['Owner'].str.lower()
df['Country/Area'] = df['Country/Area'].str.lower()
df['Technology'] = df['Technology'].str.lower()
df = df.applymap(lambda x: "N/A" if pd.isna(x) or x == '' else x)
# df['Lifetime'] = df['Lifetime'].apply(lambda x: "X" if x == "N/A" else x)

# write dataframe to excel file
df.to_excel('data_cleaned/geo_cleaned.xlsx', index=False)



