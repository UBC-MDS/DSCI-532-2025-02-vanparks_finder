from dash import callback,html, callback_context
from dash.dependencies import Input, Output, State, ALL
import ast
from ..data import parks_data

@callback(
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
