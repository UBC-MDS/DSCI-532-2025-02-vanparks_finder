import dash_bootstrap_components as dbc
from dash import html

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