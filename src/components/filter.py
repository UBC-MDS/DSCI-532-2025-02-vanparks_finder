import dash_bootstrap_components as dbc
from dash import dcc, html
from ..data import parks_data, facilities_data, special_data


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

washrooms_checkbox = dcc.Checklist(
        id="washrooms-checkbox",
        options=[{"label": " Washroom Avaliability ", "value": "Y"}],
        value=[],
        inline=True,
        style={"margin-bottom": "20px"}
    )
