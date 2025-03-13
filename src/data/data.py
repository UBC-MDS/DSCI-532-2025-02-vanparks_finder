from dash import Input, Output, callback
import dash_leaflet as dl
import pandas as pd
import json
from shapely.wkb import loads

parks_data = pd.read_parquet('src/data/processed/parks.parquet')
facilities_data = pd.read_parquet('src/data/processed/parks-facilities.parquet')
special_data = pd.read_parquet('src/data/processed/parks-special-features.parquet')


boundary_data_path = "src/data/raw/neighbourhood-boundary.geojson"

with open(boundary_data_path, "r", encoding="utf-8") as file:
    boundary_data = json.load(file)

#Start proprocessing

