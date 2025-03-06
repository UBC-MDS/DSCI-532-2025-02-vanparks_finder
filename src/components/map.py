import dash_leaflet as dl
from data import parks_data

geo_location_dict = {
    'Arbutus-Ridge': {'zoom': 14.17, 'center': [49.2467288, -123.1594228]},
    'Downtown': {'zoom': 14.54, 'center': [49.2790925, -123.1147099]},
    'Dunbar-Southlands': {'zoom': 14.02, 'center': [49.2489659, -123.1860719]},
    'Fairview': {'zoom': 14.37, 'center': [49.2654975, -123.1282056]},
    'Grandview-Woodland': {'zoom': 13.91, 'center': [49.2759762, -123.0682878]},
    'Hastings-Sunrise': {'zoom': 13, 'center': [49.2778156, -123.0422014]},
    'Kensington-Cedar Cottage': {'zoom': 14.01, 'center': [49.2471833, -123.0769395]},
    'Kerrisdale': {'zoom': 14, 'center': [49.225243, -123.16097]},
    'Killarney': {'zoom': 13.78, 'center': [49.2180367, -123.0383941]},
    'Kitsilano': {'zoom': 14.26, 'center': [49.2674605, -123.1642213]},
    'Marpole': {'zoom': 14.46, 'center': [49.2104717, -123.130635]},
    'Mount Pleasant': {'zoom': 14.63, 'center': [49.2647148, -123.0978001]},
    'Oakridge': {'zoom': 14.01, 'center': [49.226586, -123.122330]},
    'Renfrew-Collingwood': {'zoom': 13.81, 'center': [49.2483732, -123.0386256]},
    'Riley Park': {'zoom': 14.28, 'center': [49.24452, -123.1020171]},
    'Shaughnessy': {'zoom': 14.3, 'center': [49.2456008, -123.1415797]},
    'South Cambie': {'zoom': 14.1, 'center': [49.246474, -123.121238]},
    'Strathcona': {'zoom': 14.94, 'center': [49.2725961, -123.0887926]},
    'Sunset': {'zoom': 14.08, 'center': [49.2188485, -123.0911351]},
    'Victoria-Fraserview': {'zoom': 14.0, 'center': [49.222683, -123.062963]},
    'West End': {'zoom': 14.71, 'center': [49.2853688, -123.1342539]},
    'West Point Grey': {'zoom': 14, 'center': [49.266988, -123.202435]}
}


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
