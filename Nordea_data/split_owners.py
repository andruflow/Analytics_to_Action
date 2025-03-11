# import pandas as pd
# import numpy as np

# def split_owners(df):
#     """
#     Splits rows with multiple owners into separate rows, adjusting the Capacity (MW) 
#     according to the percentage owned. Also removes the rows that have several owners.
#     """
#     expanded_rows = []
#     rows_remove = []

#     for index, row in df.iterrows():
#         owners = str(row["Owner(s)"]).split(";")  # multiple owners are separated by ";"
        
#         owner_entries = []
#         for owner in owners:
#             owner = owner.strip()
#             name, percentage = owner, np.nan  # Initialize `name` and `percentage`
#             if "[100%]" in owner:
#                 df.at[index, "Owner(s)"] = owner.replace("[100%]", "").strip()
#                 continue
#             if owner.strip() == "" or owner.strip().lower() == "n/a" or (len(owners) == 1 and "[" not in owner):
#                  continue  # Skip this row
#             elif "[" in owner and "%" in owner:  # If percentage is specified
#                 name, percentage = owner.rsplit("[", 1)
#                 percentage = percentage.replace("%]", "").strip()
#                 rows_remove.append(index)
#                 percentage = float(percentage) / 100  # Convert percentage to decimal
            

#             owner_entries.append((name, percentage))
        
#         # Create new rows with adjusted capacities
#         for owner_name, pct in owner_entries:
#             new_row = row.copy()
#             new_row["Owner(s)"] = owner_name
#             new_row["Capacity (MW)"] = row["Capacity (MW)"] * pct  # Adjust capacity
#             expanded_rows.append(new_row)
    
#     df = df.drop(index=rows_remove)
#     df = df.append(expanded_rows)

#     return df

# import pandas as pd
# import numpy as np

# def split_owners(df):
#     """
#     - Splits rows with multiple owners into separate rows, adjusting the Capacity (MW) 
#         according to the percentage owned. 
#     - Removes the rows that have several owners.
#     - If an owner has 100% ownership, the "[100%]" is removed, but the row is kept.
#     """
#     expanded_rows = []
#     rows_to_remove = set()  # Use a set to avoid duplicate removals

#     updated_df = df.copy()  # Work on a copy to avoid modifying the original while iterating

#     for index, row in df.iterrows():
#         # Handle NaN or empty owner entries properly
#         owner_field = row["Owner(s)"]
#         if pd.isna(owner_field) or owner_field.strip() == "":
#             continue  # Leave empty owner rows unchanged

#         owners = owner_field.split(";")  # Multiple owners are separated by ";"
#         owner_entries = []

#         # **Check if the row has a single owner with [100%]**
#         if len(owners) == 1 and "[100%]" in owners[0]:
#             updated_df.at[index, "Owner(s)"] = owners[0].replace("[100%]", "").strip()
#             continue  # Keep the row unchanged

#         # Process multiple owners
#         for owner in owners:
#             owner = owner.strip()
#             name, percentage = owner, np.nan  # Initialize `name` and `percentage`

#             if "[" in owner and "%" in owner:  # If percentage is specified
#                 try:
#                     name, percentage = owner.rsplit("[", 1)
#                     percentage = percentage.replace("%]", "").strip()
#                     percentage = float(percentage) / 100  # Convert percentage to decimal
#                     rows_to_remove.add(index)  # Mark row for removal
#                 except ValueError:
#                     percentage = np.nan  # Handle cases where conversion fails

#             owner_entries.append((name.strip(), percentage))

#         # If no percentages are given and there is only one owner, keep the row
#         if len(owner_entries) == 1 and pd.isna(owner_entries[0][1]):
#             continue  # Skip splitting single-owner rows without percentages

#         # If the row has multiple owners, remove the original row
#         if len(owner_entries) > 1:
#             rows_to_remove.add(index)

#         # Create new rows with adjusted capacities, ensuring correct country/plant mapping
#         for owner_name, pct in owner_entries:
#             new_row = row.copy()
#             new_row["Owner(s)"] = owner_name  # Assign the correct owner name
#             new_row["Capacity (MW)"] = row["Capacity (MW)"] * pct if not pd.isna(pct) else row["Capacity (MW)"]
#             expanded_rows.append(new_row)

#     # Remove only the rows that needed to be split
#     updated_df = updated_df.drop(index=rows_to_remove).reset_index(drop=True)

#     # Append expanded rows to the cleaned DataFrame
#     updated_df = pd.concat([updated_df, pd.DataFrame(expanded_rows)], ignore_index=True)

#     return updated_df

# 

import pandas as pd
import numpy as np

def split_owners(df):
    """
    Splits rows with multiple owners into separate rows, adjusting the Capacity (MW) 
    according to the percentage owned. Also removes the rows that have several owners.
    Ensures that rows with empty "Owner" fields remain unchanged.
    If an owner has 100% ownership, the "[100%]" is removed, but the row is kept.
    """
    expanded_rows = []  # Store new rows separately before modifying df
    rows_to_remove = set()  # Use a set to track rows for removal

    # **Store Original Index to Maintain Order**
    df["Original_Index"] = df.index  

    updated_df = df.copy()  # Work on a copy to avoid modifying the original DataFrame while iterating

    for index, row in df.iterrows():
        # Handle NaN or empty owner entries properly
        owner_field = row["Owner"]
        if pd.isna(owner_field) or owner_field.strip() == "":
            continue  # Leave empty owner rows unchanged

        owners = owner_field.split(";")  # Multiple owners are separated by ";"
        owner_entries = []

        # **Check if the row has a single owner with [100%]**
        if len(owners) == 1 and "[100%]" in owners[0]:
            updated_df.at[index, "Owner"] = owners[0].replace("[100%]", "").strip()
            continue  # Keep the row unchanged

        # Process multiple owners
        for owner in owners:
            owner = owner.strip()
            name, percentage = owner, np.nan  # Initialize `name` and `percentage`

            if "[" in owner and "%" in owner:  # If percentage is specified
                try:
                    name, percentage = owner.rsplit("[", 1)
                    percentage = percentage.replace("%]", "").strip()
                    percentage = float(percentage) / 100  # Convert percentage to decimal
                    rows_to_remove.add(index)  # Mark original row for removal
                except ValueError:
                    percentage = np.nan  # Handle cases where conversion fails

            owner_entries.append((name.strip(), percentage))
        
        # **If no percentages are given, divide the capacity equally among all owners**
        if all(pd.isna(entry[1]) for entry in owner_entries):
            num_owners = len(owner_entries)
            for i in range(num_owners):
                owner_entries[i] = (owner_entries[i][0], 1 / num_owners)  # Assign equal percentages
            rows_to_remove.add(index)

        # If no percentages are given and there is only one owner, keep the row
        if len(owner_entries) == 1 and pd.isna(owner_entries[0][1]):
            continue  # Skip splitting single-owner rows without percentages

        # Create new rows with adjusted capacities, ensuring correct country/plant mapping
        for owner_name, pct in owner_entries:
            new_row = row.copy()  # Copy the row to avoid modifying the original row
            new_row["Owner"] = owner_name  # Assign the correct owner name
            new_row["Capacity (MW)"] = row["Capacity (MW)"] * pct if not pd.isna(pct) else row["Capacity (MW)"]
            expanded_rows.append(new_row)

    # **Drop rows only after all splits are done** to avoid index shifting
    updated_df = updated_df.drop(index=rows_to_remove)

    # **Append expanded rows separately** to avoid index mismatch
    expanded_df = pd.DataFrame(expanded_rows)

    # **Ensure original indexing order before finalizing**
    if not expanded_df.empty:
        updated_df = pd.concat([updated_df, expanded_df], ignore_index=True)

    # **Sort by the stored Original_Index to maintain order**
    updated_df = updated_df.sort_values(by="Original_Index").drop(columns=["Original_Index"]).reset_index(drop=True)

    return updated_df
