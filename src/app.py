from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
# src/app.py
from .components import *
from . import callbacks


# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server




# Define the layout with a map centered on Vancouver
app.layout = dbc.Container(
    fluid=True,
    style={"padding": "20px"},
    children=[
        dbc.Row([
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
                    num_parks_card
                ]
            ),
            dbc.Col(
                width=9,
                children=[
                    park_map,
                    dbc.Row([
                        dbc.Col(
                            html.Div(
                                bar_chart,
                                style={
                                    "width": "70%",
                                    "display": "inline-block",
                                    "verticalAlign": "top"
                                }
                            ),
                            width=10
                        ),
                        dbc.Col(
                            html.Div(
                                dcc.Markdown(
                                    """
                                    This dashboard was made to help park enthusiasts find parks 
                                    suited to their preferences in Vancouver. Created by Inder Khera, 
                                    Timothy Singh, Ximin Xu, Shengjia Yu. The GitHub Repo can be found 
                                    [here.](https://github.com/UBC-MDS/DSCI-532-2025-02-vanparks_finder)
                                    Latest Deployment Date: 2025-02-28
                                    """
                                ),
                                style={
                                    "fontSize": "6.3px",
                                    "textAlign": "left",
                                    "marginTop": "60px",
                                    "marginRight": "7px"
                                }
                            ),
                            width=2
                        )
                    ])
                ]
            )
        ])
    ]
)




if __name__ == '__main__':
    app.server.run(debug=False, port=8000, host='127.0.0.1')