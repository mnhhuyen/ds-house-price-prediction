import pandas as pd
import os
import re

def extract_address_components(address):
    if not isinstance(address, str):
        return ["", "", ""]

    # Split address into parts
    parts = re.split(r'[\s,-]+', address)
    parts = [part.strip() for part in parts if part.strip()]
    
    # Initialize default values
    street, ward, district = "", "", ""

    if len(parts) == 1 and not any(kw in parts[0].lower() for kw in ['đường', 'phường', 'quận']):
        return [parts[0], "", ""]
    # Check if address has 3 parts
    if len(parts) == 3:
        return parts
    elif len(parts) == 2:
        return [parts[0], parts[1], ""]
    else:
        # Regular expressions for street and ward
        street_pattern = r'Đường\s*([^,Phường]+)'
        ward_pattern = r'Phường\s*([^,]+)'

        # Extract ward first
        ward_match = re.search(ward_pattern, address, re.IGNORECASE)
        if ward_match:
            ward = ward_match.group(1).strip()
            # Update street pattern if ward is found
            street_pattern = r'Đường\s*([^,]+?)(?=, Phường| Phường)'

        # Extract street
        street_match = re.search(street_pattern, address, re.IGNORECASE)
        if street_match:
            street = street_match.group(1).strip()

        # Extract district if it follows the ward, or take the last part of the address
        if ward and len(parts) > 1:
            district = parts[-1].strip()
        elif len(parts) > 3:
            district = parts[-1].strip()

    return [street, ward, district]


def convert_price(price_str, area):
    if not isinstance(price_str, str):
        return None
    price_str = price_str.replace(',', '.').strip()
    if '/tháng' in price_str:
        return None
    if 'tỷ' in price_str:
        price_str = price_str.replace(' tỷ VNĐ', '').replace(' tỷ', '')
        try:
            return float(price_str) * 1000
        except ValueError:
            return None
    elif 'triệu' in price_str:
        try:
            return float(price_str.replace(' triệu VNĐ', '').replace(' triệu', ''))
        except ValueError:
            return None
    elif '/m2' in price_str:
        try:
            price_per_m2 = float(price_str.replace('/m2', ''))
            return price_per_m2 * area
        except ValueError:
            return None
    else:
        return None

def clean_direction(direction_str):
    direction_map = {
        'đông': 'E', 'tây': 'W', 'nam': 'S', 'bắc': 'N',
        'tây bắc': 'WN', 'tây nam': 'WS', 'đông bắc': 'EN', 'đông nam': 'ES'
    }
    direction_str = direction_str.lower().strip() if isinstance(direction_str, str) else direction_str
    return direction_map.get(direction_str, "")

def determine_furniture(details):
    if isinstance(details, str) and 'nội thất' in details:
        return 1
    return 0

def clean_legitimacy(details):
    if isinstance(details, str) and 'sổ' in details:
        return 2
    return 0

folder_path = '/home/nmh/ds/project/data/batdongsanso'
all_dfs = []

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        df[['street', 'ward', 'district']] = df['address'].fillna("").apply(lambda x: pd.Series(extract_address_components(x)))
        df['city'] = 'Hà Nội'

        df['area'] = df['Diện tích'].str.replace('m2', '').str.strip().astype(float).fillna(0)

        df['price'] = df.apply(lambda row: convert_price(row['price'], row['area']), axis=1)

        if 'Hướng' in df.columns and df['Hướng'].notnull().any():
            df['house_direction'] = df['Hướng'].apply(clean_direction)
        else:
            df['house_direction'] = None

        if 'Hướng ban công' in df.columns:
            df['balcony_direction'] = df['Hướng ban công'].apply(clean_direction)
        else:
            df['balcony_direction'] = None

        if 'Số phòng ngủ' in df.columns:
            df['bedroom'] = pd.to_numeric(df['Số phòng ngủ'], errors='coerce')
        else:
            df['bedroom'] = None

        if 'Số toilet' in df.columns:
            df['toilet'] = pd.to_numeric(df['Số toilet'], errors='coerce')
        else:
            df['toilet'] = None

        if 'Số tầng' in df.columns:
            df['floors'] = pd.to_numeric(df['Số tầng'], errors='coerce')
        else:
            df['floors'] = None

        df['furniture'] = df['Details'].apply(determine_furniture)
        df['legits'] = df['Details'].apply(clean_legitimacy)

        df['facade'] = pd.to_numeric(df['Mặt tiền'], errors='coerce') if 'Mặt tiền' in df.columns else None
        df['entrance'] = pd.to_numeric(df['Lộ giới'], errors='coerce') if 'Lộ giới' in df.columns else None

        df = df[df['price'].notnull()]

        final_columns = ['id', 'city', 'district', 'ward', 'street', 'area', 'price', 'house_direction', 
                         'balcony_direction', 'bedroom', 'toilet', 'floors', 'legits', 'furniture', 
                         'facade', 'entrance']
        df_final = df[final_columns]
        all_dfs.append(df_final)

combined_df = pd.concat(all_dfs, ignore_index=True)
combined_df.to_csv('cleaned_data.csv', index=False)
