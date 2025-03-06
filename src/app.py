from dash import Dash, html, dcc, callback_context
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from components import bar_chart, map, filter
import callbacks
import pandas as pd
import ast
from dash.dependencies import Input, Output, State, ALL

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
parks_data = pd.read_csv('data/raw/parks.csv', delimiter =';')
facilities_data = pd.read_csv('data/raw/parks-facilities.csv', delimiter=';')
special_data = pd.read_csv('data/raw/parks-special-features.csv', delimiter=';')

parks_data['Coordinates'] = parks_data['GoogleMapDest'].apply(ast.literal_eval)

parks_data[['Latitude', 'Longitude']] = pd.DataFrame(parks_data['Coordinates'].to_list(), index=parks_data.index)
#dropdown options
neighborhood_options = [
    {"label": nbhd, "value": nbhd}
    for nbhd in sorted(parks_data["NeighbourhoodName"].dropna().unique())
]
facility_options = [
    {"label": ftype, "value": ftype}
    for ftype in sorted(facilities_data["FacilityType"].dropna().unique())
]
special_features_options = [
    {"label": sfeat, "value": sfeat}
    for sfeat in sorted(special_data["SpecialFeature"].dropna().unique())
]

avg_hectare_card = dbc.Card(
    dbc.CardBody([
        html.H5("Average Hectare per Park:", className="card-title"),
        html.H2(id="avg-hectare-text", className="card-text text-center")
    ]),
    className="mt-4"
)

num_parks_card = dbc.Card(
    dbc.CardBody([
        html.H5("Number of Parks:", className="card-title"),
        html.H2(id="num-parks-text", className="card-text text-center"),
        
    ]),
    className="mt-4"
)

park_info_modal = dbc.Modal(
    id="park-info-modal",
    children=[
        dbc.ModalHeader("Selected Park Details"),
        dbc.ModalBody(id="park-info"),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-park-modal", className="ml-auto", n_clicks=0)
        ),
    ],
    is_open=False,  
    size="lg", 
)
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

# Define the layout with a map centered on Vancouver
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        # Left Column: Filters (imported from components/filters.py)
        filter.create_filters(
            neighborhood_options,
            facility_options,
            special_features_options
        ),

        # Right Column: Map + Bar Chart
        dbc.Col(width=9, children=[
            park_map,
            bar_chart
        ]),
    ]),
    dbc.Row([
        dcc.Markdown("""
            This dashboard was made to help park enthusiasts find parks suited to their preferences in Vancouver. 
            Created by Inder Khera, Timothy Singh, Ximin Xu, Shengjia Yu.

            The GitHub Repo can be found [here.](https://github.com/UBC-MDS/DSCI-532-2025-02-vanparks_finder) 
            Latest Deployment Date: 2025-02-28
        """)
    ])
], style={"padding": "20px"})


@app.callback(
    Output("park-info", "children"),
    Output("park-info-modal", "is_open"),
    Input({'type': 'park-marker', 'index': ALL}, "n_clicks"),
    Input("close-park-modal", "n_clicks"),
    prevent_initial_call=True
)
def update_park_info(n_clicks, close_click):
    ctx = callback_context

    if ctx.triggered[0]["prop_id"] == "close-park-modal.n_clicks":
        return "", False

    if not ctx.triggered or not any(n_clicks):  
        return "Click on a park to see details.", False

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    try:
        park_id = ast.literal_eval(triggered_id)["index"]
    except Exception:
        return "Error parsing park selection.", False

    if park_id not in parks_data["ParkID"].values:
        return "Selected park not found.", True

    park = parks_data[parks_data["ParkID"] == park_id].iloc[0]

    return html.Div([
        html.B("Name: "), f"{park['Name']}", html.Br(),
        html.B("Street Number: "), f"{park['StreetNumber']}", html.Br(),
        html.B("Street Name: "), f"{park['StreetName']}", html.Br(),
        html.B("Neighbourhood: "), f"{park['NeighbourhoodName']}", html.Br(),
        html.B("Hectare: "), f"{park['Hectare']:.2f}", html.Br(),
        html.B("Washroom: "), f"{park['Washrooms']}"
    ]), True  


if __name__ == '__main__':
    app.server.run(debug=False, port=8000, host='127.0.0.1')