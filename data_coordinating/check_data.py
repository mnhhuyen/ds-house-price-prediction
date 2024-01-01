import pandas as pd
import numpy as np

csv_file_path = '/home/nmh/ds/project/data_ver3_coordinated.csv'
data = pd.read_csv(csv_file_path)
output_path = '/home/nmh/ds/project/data_ver3_coordinated_filtered_ver1.csv'

def count_complete_rows(csv_file_path):
    data = pd.read_csv(csv_file_path)
    complete_rows = data.dropna(subset=['latitude','longitude'])
    num_complete_rows = len(complete_rows)
    return num_complete_rows
# csv_file_path = '/home/nmh/ds/project/data_ver3_coordinated.csv'
print("Number of complete rows:" ,count_complete_rows(csv_file_path))

def filter(csv_file_path):
    for col in data.columns:
        if data[col].dtype == 'object':  
            data[col].fillna('None', inplace=True)
        else:
            # data[col].fillna(data[col].median(), inplace=True)
            data[col].fillna(np.nan, inplace=True) 
    # output_path = '/home/nmh/ds/project/data_ver3_coordinated_filtered.csv'
    data.to_csv(output_path, index=False)
filter(csv_file_path)
print(count_complete_rows(output_path))