import dash_bootstrap_components as dbc
from dash import dcc, html

def create_filters(neighborhood_options, facility_options, special_features_options):
    """Create and return a column of filter components."""
    # Dropdowns
    neighbourhood_dropdown = dcc.Dropdown(
        id="neighbourhood-dropdown",
        options=neighborhood_options,
        value=None,
        placeholder="Select a neighbourhood...",
        multi=False,
        clearable=True,
        searchable=True,
        style={"margin-bottom": "20px"}
    )
    facility_dropdown = dcc.Dropdown(
        id="facility-dropdown",
        options=facility_options,
        value=[],
        placeholder="Select facility type(s)...",
        multi=True,
        clearable=True,
        style={"margin-bottom": "20px"}
    )
    special_feature_dropdown = dcc.Dropdown(
        id="special-feature-dropdown",
        options=special_features_options,
        value=[],
        placeholder="Select special feature(s)...",
        multi=True,
        clearable=True,
        style={"margin-bottom": "20px"}
    )

    # Washrooms
    washrooms_checkbox = dcc.Checklist(
        id="washrooms-checkbox",
        options=[{"label": " Washroom Avaliability ", "value": "Y"}],
        value=[],
        inline=True,
        style={"margin-bottom": "20px"}
    )

    # Cards
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

    # Modal
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

    # Return filters in a Column
    return dbc.Col(
        width=3,
        children=[
            html.H1("Vanparks Finder"),
            html.Label("Neighbourhood Name"),
            neighbourhood_dropdown,
            html.Label("Facility Type"),
            facility_dropdown,
            html.Label("Special Feature"),
            special_feature_dropdown,
            washrooms_checkbox,
            park_info_modal,
            avg_hectare_card,
            num_parks_card,
        ],
    )
