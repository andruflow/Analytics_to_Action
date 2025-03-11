import pandas as pd
import numpy as np

# def findCapacity(file_path):
#     df = pd.read_excel(file_path, sheet_name='Data')
#     capacities = df['Capacity (MW)'].to_numpy()
#     owners = df['Owner'].to_numpy()
#     df_local = pd.DataFrame({"Owner": owners, "Capacity": capacities})
    
#     # Group by owner and sum capacity
#     result = df_local.groupby("Owner")["Capacity"].sum().reset_index()
    
#     return result


def findCapacity(file_path):
    df = pd.read_excel(file_path, sheet_name='Data')

    # Ensure correct data types
    df['Owner'] = df['Owner'].astype(str)
    df['Capacity (MW)'] = pd.to_numeric(df['Capacity (MW)'], errors='coerce').fillna(0)

    # Group by owner and sum capacity
    result = df.groupby("Owner", as_index=False)["Capacity (MW)"].sum()

    return result



geo_capacity_dist = findCapacity('Geothermal-Power-Tracker-May-2024.xlsx')
#bio_capacity_dist = findCapacity('Global-Bioenergy-Power-Tracker-GBPT-September-2024.xlsx')
#coal_capacity_dist = findCapacity('Global-Coal-Plant-Tracker-January-2025.xlsx')
hydro_capacity_dist = findCapacity('Global-Hydropower-Tracker-April-2024.xlsx')
#nuclear_capacity_dist = findCapacity('Global-Nuclear-Power-Tracker-July-2024.xlsx')
#oilgas_capacity_dist = findCapacity('Global-Oil-and-Gas-Plant-Tracker-GOGPT-January-2025.xlsx')
#solar_capacity_dist = findCapacity('Global-Solar-Power-Tracker-February-2025')
#wind_capacity_dist = findCapacity('Global-Wind-Power-Tracker-February-2025')

#print(hydro_capacity_dist)


#### plot the five biggest owners for each power plant type #####



geo_total = geo_capacity_dist['Capacity (MW)'].sum()
hydro_total = hydro_capacity_dist['Capacity (MW)'].sum()
print(hydro_total)