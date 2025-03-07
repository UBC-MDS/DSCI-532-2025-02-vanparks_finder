# imports
from data import parks_data, facilities_data, special_data
from dash import Input, Output, callback
from ..components.bar_chart import create_bar_chart

@callback(
    Output("bar-chart", "spec"),
    Input("neighbourhood-dropdown", "value"),
    Input("facility-dropdown", "value"),
    Input("special-feature-dropdown", "value"),
    Input("washrooms-checkbox", "value")
)
def update_bar_chart(selected_neighbourhood, selected_facilities, selected_special_features, washroom_filter):
    df_filtered = parks_data.copy()

    # Filter by neighbourhood
    if selected_neighbourhood:
        df_filtered = df_filtered[df_filtered["NeighbourhoodName"] == selected_neighbourhood]

    # Filter by washroom availability
    if washroom_filter is None:
        washroom_filter = []
    
    if "Y" in washroom_filter:
        df_filtered = df_filtered[df_filtered["Washrooms"] == "Y"]

    park_ids = set(df_filtered["ParkID"])

    # Ensure parks contain *all* selected facilities
    if selected_facilities:
        facility_counts = facilities_data[facilities_data["FacilityType"].isin(selected_facilities)]
        facility_counts = facility_counts.groupby("ParkID")["FacilityType"].nunique()
        matching_facilities = set(facility_counts[facility_counts == len(selected_facilities)].index)
        park_ids &= matching_facilities if park_ids else matching_facilities  

    # Ensure parks contain *all* selected special features
    if selected_special_features:
        special_counts = special_data[special_data["SpecialFeature"].isin(selected_special_features)]
        special_counts = special_counts.groupby("ParkID")["SpecialFeature"].nunique()
        matching_specials = set(special_counts[special_counts == len(selected_special_features)].index)
        park_ids &= matching_specials if park_ids else matching_specials  

    # Only filter for specific ParkIDs
    facilities_data_new = facilities_data[facilities_data["ParkID"].isin(park_ids)]

    # Update Chart
    return create_bar_chart(facilities_data_new)