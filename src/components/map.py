import dash_leaflet as dl
from data import parks_data


def create_markers(df):
    return [
        dl.Marker(
            position=[row["Latitude"], row["Longitude"]],
            id={'type': 'park-marker', 'index': row["ParkID"]},
            children=dl.Popup(f"Park: {row['Name']}"),
            n_clicks=0
        )
        for _, row in df.iterrows()
    ]

park_map = dl.Map(
    children=[dl.TileLayer()],
    id="vancouver-map",
    center=[49.2827, -123.1207],
    zoom=12,
    style={'height': '70vh'},
    maxZoom=18,
    minZoom=12,
    maxBounds=[[49.1, -123.3], [49.5, -122.7]],
    dragging=True,
    zoomControl=True
)
