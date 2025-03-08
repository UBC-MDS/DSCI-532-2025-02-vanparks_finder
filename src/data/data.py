import pandas as pd
import ast
import json

parks_data = pd.read_csv('data/raw/parks.csv', delimiter =';')
parks_data['Coordinates'] = parks_data['GoogleMapDest'].apply(ast.literal_eval)
parks_data[['Latitude', 'Longitude']] = pd.DataFrame(parks_data['Coordinates'].to_list(), index=parks_data.index)

facilities_data = pd.read_csv('data/raw/parks-facilities.csv', delimiter=';')
special_data = pd.read_csv('data/raw/parks-special-features.csv', delimiter=';')

boundary_data_path = "data/raw/neighbourhood-boundary.geojson"
with open(boundary_data_path) as file:
    boundary_data= json.load(file)