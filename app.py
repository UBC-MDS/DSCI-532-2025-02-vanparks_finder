from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import pandas as pd
import ast

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

parks_data = pd.read_csv('data/raw/parks.csv', delimiter =';')

parks_data['Coordinates'] = parks_data['GoogleMapDest'].apply(ast.literal_eval)

parks_data[['Latitude', 'Longitude']] = pd.DataFrame(parks_data['Coordinates'].to_list(), index=parks_data.index)

markers = [
    dl.Marker(position=[row['Latitude'], row['Longitude']], children=dl.Popup(f"Park: {row['Name']}"))
    for _, row in parks_data.iterrows()
]



map_component = dl.Map(
    children=[
        dl.TileLayer(),
         *markers  
    ],
    center=[49.2827, -123.1207],  
    zoom=12,  
    style={'height': '50vh'},  
    maxZoom=18,  
    minZoom=12, 
    maxBounds=[[49.1, -123.3], [49.5, -122.7]], 
    dragging=True,  
    zoomControl=True  
)


# Define the layout with a map centered on Vancouver
app.layout = dbc.Container([
    html.H1("Vancouver Parks Map"),
    html.Div([map_component])
])


if __name__ == '__main__':
    app.server.run(debug=True, port=8000, host='127.0.0.1')