from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from components import bar_chart, park_map, neighbourhood_dropdown, facility_dropdown, special_feature_dropdown, washrooms_checkbox, avg_hectare_card, num_parks_card, park_info_modal
import callbacks


# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server




# Define the layout with a map centered on Vancouver
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        # Left Column: Filters (imported from components/filters.py)
        dbc.Col(
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



if __name__ == '__main__':
    app.server.run(debug=False, port=8000, host='127.0.0.1')