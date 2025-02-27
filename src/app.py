from dash import Dash, html, dcc, Input, Output, callback,callback_context
from dash.dependencies import ALL
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import pandas as pd
import ast

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

parks_data = pd.read_csv('../data/raw/parks.csv', delimiter =';')
facilities_data = pd.read_csv('../data/raw/parks-facilities.csv', delimiter=';')
special_data = pd.read_csv('../data/raw/parks-special-features.csv', delimiter=';')

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
        html.H2(id="num-parks-text", className="card-text text-center")
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


# Define the layout with a map centered on Vancouver
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        # Left Column: Filters
        dbc.Col(width=3, children=[
            html.H1("Vancouver Parks Map"),
            html.Label("Neighbourhood Name"),
            dcc.Dropdown(
                id="neighbourhood-dropdown",
                options=neighborhood_options,
                value=None,             # No default selection
                placeholder="Select a neighbourhood...",
                multi=False,           # Single selection
                clearable=True,
                searchable=True,       # Allows search in the dropdown
                style={"margin-bottom": "20px"}
            ),

            html.Label("Facility Type"),
            dcc.Dropdown(
                id="facility-dropdown",
                options=facility_options,
                value=[],              # No default selection
                placeholder="Select facility type(s)...",
                multi=True,           # Multi selection
                clearable=True,
                style={"margin-bottom": "20px"}
            ),

            html.Label("Special Feature"),
            dcc.Dropdown(
                id="special-feature-dropdown",
                options=special_features_options,
                value=[],              # No default selection
                placeholder="Select special feature(s)...",
                multi=True,           # Multi selection
                clearable=True,
                style={"margin-bottom": "20px"}
            ),
            html.Label("Washroom Avaliability"),
            dcc.Checklist(
                id="washrooms-checkbox",
                options=[{"label": "  Yes ", "value": "Y"}],
                value=[],  # Default: unchecked (show all parks)
                inline=True,
                style={"margin-bottom": "20px"}
            )
        ]),

        # Right Column: Map
        dbc.Col(width=6, children=[

            dl.Map(
                children=[
                    dl.TileLayer()
                    ],
                id="vancouver-map",
                center=[49.2827, -123.1207], 
                zoom=12,
                style={'height': '70vh'}, # This is controling the height of the map
                maxZoom=18,
                minZoom=12,
                maxBounds=[[49.1, -123.3], [49.5, -122.7]],
                dragging=True,
                zoomControl=True
            )
        ]),
         dbc.Col(width=3, children=[
            park_info_modal,
            avg_hectare_card,
            num_parks_card
        ])
    ]),
    park_info_modal 
],
    style={"padding": "20px"} # This is controling the page style
    )

@app.callback(
    Output("vancouver-map", "children"),
    Output("num-parks-text", "children"),
    Output("avg-hectare-text", "children"),
    Input("neighbourhood-dropdown", "value"),
    Input("facility-dropdown", "value"),
    Input("special-feature-dropdown", "value"),
    Input("washrooms-checkbox", "value")
)
def update_map(selected_neighbourhood, selected_facilities, selected_special_features, washroom_filter):
    # Instead of interesecting, this function is currently adding parkID for filtering. 
    # For example: user input 2 features, instead of filtering out the park with both features, the callback is outputting park with feature 1 or feature 2
    # Same for facilities
    df_filtered = parks_data.copy()
    # Filter by neighbourhood
    if selected_neighbourhood:
        df_filtered = df_filtered[df_filtered["NeighbourhoodName"] == selected_neighbourhood]

    # Filter by washroom avaliability
    if washroom_filter is None:
        washroom_filter = []
    
    if "Y" in washroom_filter:
        df_filtered = df_filtered[df_filtered["Washrooms"] == "Y"]

    park_ids = set(df_filtered["ParkID"])
    # Filter by facility types
    if selected_facilities:
        matching_facilities = set(facilities_data.loc[facilities_data["FacilityType"].isin(selected_facilities), "ParkID"])
        park_ids &= matching_facilities if park_ids else matching_facilities  
    
    if selected_special_features:
        matching_specials = set(special_data.loc[special_data["SpecialFeature"].isin(selected_special_features), "ParkID"])
        park_ids &= matching_specials if park_ids else matching_specials  
    # Apply the final filter once
    df_filtered = df_filtered[df_filtered["ParkID"].isin(park_ids)]

    num_parks_filtered = df_filtered["ParkID"].nunique()
    avg_hectare_filtered = df_filtered["Hectare"].mean()

    num_parks_text = str(num_parks_filtered) if num_parks_filtered > 0 else "0"
    avg_hectare_text = f"{avg_hectare_filtered:.2f}" if not df_filtered.empty else "0.00"

    return [dl.TileLayer()] + create_markers(df_filtered) if not df_filtered.empty else [dl.TileLayer()], num_parks_text, avg_hectare_text

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
    app.server.run(debug=True, port=8000, host='127.0.0.1')