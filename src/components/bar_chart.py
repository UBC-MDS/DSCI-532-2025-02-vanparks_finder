# imports
import altair as alt
import dash_vega_components as dvc

from data import facilities_data

def create_bar_chart(data):
    parks_chart_filter = data.groupby("FacilityType").sum().reset_index()[["FacilityType", "FacilityCount"]]
    parks_chart_filter = parks_chart_filter.sort_values(by="FacilityCount", ascending=False)[:5]
    alt.theme.enable("fivethirtyeight")

    chart = alt.Chart(parks_chart_filter).mark_bar().encode(
        x=alt.X('FacilityCount:Q').scale(nice=True).axis(format='d'),
        y=alt.Y('FacilityType:N').sort('-x'),
        color=alt.Color('FacilityType', legend=None),
        tooltip = ['FacilityType','FacilityCount']
    ).configure(
        background="transparent",
    ).configure_axis(
        labelColor= "black",
        titleColor= "grey",
        labelFontSize=12,
        titleFontSize=12,
        labelFontStyle='Helvetica'
    ).properties(
        title="Top 5 Facilities",
        width=550,
        height=80
    ).configure_title(
        font='Helvetica',
        fontSize=16,
        anchor='start',
    )

    return chart.to_dict()

bar_chart = dvc.Vega(
    id="bar-chart",
    spec=create_bar_chart(facilities_data),
    style={'width': '100%'}
)