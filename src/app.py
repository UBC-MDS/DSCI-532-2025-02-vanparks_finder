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
num_parks = parks_data['ParkID'].nunique()
avg_hectare = parks_data['Hectare'].mean()

avg_hectare_card = dbc.Card(
    dbc.CardBody([
        html.H5("Average Hectare per Park:", className="card-title"),
        html.H2(f"{avg_hectare:.2f}", className="card-text text-center")
    ]),
    className="mt-4"
)

num_parks_card = dbc.Card(
    dbc.CardBody([
        html.H5("Number of Parks:", className="card-title"),
        html.H2(f"{num_parks}", className="card-text text-center")
    ]),
    className="mt-4"
)

park_info_card = dbc.Card(
    dbc.CardBody([
        html.H4("Selected Park", className="card-title"),
        html.Div("Click on a park to see details.", id="park-info", className="card-text")
    ]),
    className="mt-4"
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
            park_info_card,
            avg_hectare_card,
            num_parks_card
        ])
    ])
    
],
    style={"padding": "20px"} # This is controling the page style
    )

@app.callback(
    Output("vancouver-map", "children"),
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
 # Keep only matching park IDs

    # Apply the final filter once
    df_filtered = df_filtered[df_filtered["ParkID"].isin(park_ids)]

    return [dl.TileLayer()] + create_markers(df_filtered) if not df_filtered.empty else [dl.TileLayer()]

    # df_filtered will become a parks df with only parkID filtered
    # The variable parks_ids contains all the filtered ParkID, you can use it for the rest of the work.

    # Create markers for the filtered parks
@app.callback(
    Output("park-info", "children"),
    Input({'type': 'park-marker', 'index': ALL}, "n_clicks")
)

def update_park_info(n_clicks):
    ctx = callback_context

    if not ctx.triggered or not n_clicks or all(n is None or n == 0 for n in n_clicks):
        return "Click on a park to see details."

    try:
        triggered_id = ast.literal_eval(ctx.triggered[0]['prop_id'].split('.')[0])
        park_id = triggered_id['index']
    except Exception as e:
        return f"Error parsing park selection: {e}"

    if park_id not in parks_data['ParkID'].values:
        return "Selected park not found."

    park = parks_data[parks_data['ParkID'] == park_id].iloc[0]

    return html.Div([
        html.B("Name: "), f"{park['Name']}", html.Br(),
        html.B("Street Number: "), f"{park['StreetNumber']}", html.Br(),
        html.B("Street Name: "), f"{park['StreetName']}", html.Br(),
        html.B("Neighbourhood: "), f"{park['NeighbourhoodName']}", html.Br(),
        html.B("Hectare: "), f"{park['Hectare']:.2f}", html.Br(),
        html.B("Washroom: "), f"{park['Washrooms']}"
    ])

if __name__ == '__main__':
    app.server.run(debug=True, port=8000, host='127.0.0.1')