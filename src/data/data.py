import pandas as pd

parks_data = pd.read_csv('data/raw/parks.csv', delimiter =';')
facilities_data = pd.read_csv('data/raw/parks-facilities.csv', delimiter=';')
special_data = pd.read_csv('data/raw/parks-special-features.csv', delimiter=';')