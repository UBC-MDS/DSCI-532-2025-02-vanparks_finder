from shapely.wkb import loads
import pandas as pd
import requests
import os

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

save_dir = 'src/data/raw'
parks_data = download_parquet(parks_url, save_dir, "parks.parquet")
facilities_data = download_parquet(facilities_url, save_dir, "parks-facilities.parquet")
special_data = download_parquet(special_features_url, save_dir, "parks-special-features.parquet")


parks_data = pd.read_parquet('src/data/raw/parks.parquet')
parks_data['Coordinates'] = parks_data['googlemapdest'].apply(lambda x: loads(x) if isinstance(x, bytes) else None)

parks_data['Latitude'] = parks_data['Coordinates'].apply(lambda p: p.y if p else None)
parks_data['Longitude'] = parks_data['Coordinates'].apply(lambda p: p.x if p else None)

facilities_data = pd.read_parquet('src/data/raw/parks-facilities.parquet')
special_data = pd.read_parquet('src/data/raw/parks-special-features.parquet')

boundary_data_path = "src/data/raw/neighbourhood-boundary.geojson"
response = requests.get(boundary_url)
response.raise_for_status()
with open(boundary_data_path, "wb") as f:
    f.write(response.content)
