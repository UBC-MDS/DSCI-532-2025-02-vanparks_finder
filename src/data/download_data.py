
import pandas as pd
import requests
import re
import os
from shapely.wkb import loads
import json


parks_url = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/parks/exports/parquet?lang=en&timezone=America%2FLos_Angeles'
facilities_url = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/parks-facilities/exports/parquet?lang=en&timezone=America%2FLos_Angeles'
special_features_url = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/parks-special-features/exports/parquet?lang=en&timezone=America%2FLos_Angeles'
boundary_url = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/exports/geojson?lang=en&timezone=America%2FLos_Angeles'

def download_parquet(url, save_dir, filename):
    save_path = os.path.join(save_dir, filename)  
    os.makedirs(save_dir, exist_ok=True)  
    data = pd.read_parquet(url)
    data.to_parquet(save_path, index=False)
    return data

save_dir = 'data/raw'
parks_data = download_parquet(parks_url, save_dir, "parks.parquet")
facilities_data = download_parquet(facilities_url, save_dir, "parks-facilities.parquet")
special_data = download_parquet(special_features_url, save_dir, "parks-special-features.parquet")

boundary_data_path = "data/raw/neighbourhood-boundary.geojson"
response = requests.get(boundary_url)
response.raise_for_status()
with open(boundary_data_path, "w", encoding="utf-8") as f:
    f.write(response.text)
parks_data = pd.read_parquet('data/raw/parks.parquet')
parks_data['Coordinates'] = parks_data['googlemapdest'].apply(lambda x: loads(x) if isinstance(x, bytes) else None)

parks_data['Latitude'] = parks_data['Coordinates'].apply(lambda p: p.y if p else None)
parks_data['Longitude'] = parks_data['Coordinates'].apply(lambda p: p.x if p else None)

facilities_data = pd.read_parquet('data/raw/parks-facilities.parquet')
special_data = pd.read_parquet('data/raw/parks-special-features.parquet')


boundary_data_path = "data/raw/neighbourhood-boundary.geojson"

with open(boundary_data_path, "r", encoding="utf-8") as file:
    boundary_data = json.load(file)

parks_data.rename(columns={
    "parkid": "ParkID",
    "name": "Name",
    "official": "Official",
    "advisories": "Advisories",
    "specialfeatures": "SpecialFeatures",
    "facilities": "Facilities",
    "washrooms": "Washrooms",
    "streetnumber": "StreetNumber",
    "streetname": "StreetName",
    "ewstreet": "EWStreet",
    "nsstreet": "NSStreet",
    "neighbourhoodname": "NeighbourhoodName",
    "neighbourhoodurl": "NeighbourhoodURL",
    "hectare": "Hectare"
}, inplace=True)

facilities_data.rename(columns={
    "parkid": "ParkID",
    "name": "Name",
    "facilitytype": "FacilityType",
    "facilitycount": "FacilityCount"
}, inplace=True)

special_data.rename(columns={
    "specialfeature": "SpecialFeature",
    "parkid": "ParkID",
    "name": "Name",
}, inplace=True)

parks_data = parks_data[
    ["ParkID", "Name", "SpecialFeatures", "Facilities", "Washrooms", 
     "StreetNumber", "StreetName", "NeighbourhoodName", "Hectare", "Latitude", "Longitude"]
]
def clean_special_features(value):
    if isinstance(value, str):  
        return re.sub(r"\s*\(.*?\)", "", value)  
    return value

special_data["SpecialFeature"] = special_data["SpecialFeature"].apply(clean_special_features)

processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)
parks_data.to_parquet(os.path.join(processed_dir, "parks.parquet"), index=False)
facilities_data.to_parquet(os.path.join(processed_dir, "parks-facilities.parquet"), index=False)
special_data.to_parquet(os.path.join(processed_dir, "parks-special-features.parquet"), index=False)
