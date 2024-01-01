import pandas as pd

df1 = pd.read_csv('/home/nmh/ds/project/data_cleaning_batdongsan/batdongsan_clean_v4.csv')

df2 = pd.read_csv('/home/nmh/ds/project/data_cleaning_batdongsanso/cleaned_data.csv')

df3 = pd.read_csv('/home/nmh/ds/project/data_cleaning_homedy/cleaned_data.csv')    

# Rename columns for consistency
df2.rename(columns={'id': 'index'}, inplace=True)
df1.rename(columns={'bacolny_direction': 'balcony_direction'}, inplace=True)

# Define the desired column order
desired_order = ['upload_date','house_direction', 'bedroom', 'toilet', 'legits', 'furniture', 'floors', 'facade', 'entrance', 'city', 'district', 'ward', 'street', 'area', 'price']

# Reorder columns in both DataFrames
df1 = df1[desired_order]
df2 = df2[desired_order]
df3 = df3[desired_order]

# Drop existing index columns to avoid confusion
df1.drop(columns=['index'], errors='ignore', inplace=True)
df2.drop(columns=['index'], errors='ignore', inplace=True)
df2.drop(columns=['id'], errors='ignore', inplace=True)

# Concatenate DataFrames with reset index
concatenated_df = pd.concat([df1, df2, df3], ignore_index=True)

# Add a new sequential index column
concatenated_df.reset_index(inplace=True)
concatenated_df.rename(columns={'index': 'new_index'}, inplace=True)

# Ensure the 'new_index' column is the first column
column_order = ['new_index'] + [col for col in concatenated_df.columns if col != 'new_index']
concatenated_df = concatenated_df[column_order]

# Save the concatenated DataFrame to a new CSV file
concatenated_df.to_csv('/home/nmh/ds/project/data_validation/concatenated_data.csv', index=False)
