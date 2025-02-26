import altair as alt
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd

from dash import Dash



# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the data
parks = pd.read_csv("data/raw/parks-facilities.csv", sep=";")


# Filter data (to be fixed with callbacks)
parks_filter = parks.groupby("FacilityType").sum().reset_index()[["FacilityType", "FacilityCount"]]
parks_filter = parks_filter.sort_values(by="FacilityCount", ascending=False)[:5]


chart = alt.Chart(parks_filter).mark_bar().encode(
    x='FacilityCount',
    y=alt.Y('FacilityType:N').sort('-x'),
    color=alt.Color('FacilityType', legend=None)
)

# Layout
app.layout = dbc.Container([
    # Note that you need to pass the chart as a dictionary via `to_dict()`
    dvc.Vega(spec=chart.to_dict()),
])

# Server side callbacks/reactivity
# ...

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)