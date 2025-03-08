from dash import Input, Output, callback
import dash_leaflet as dl
import pandas as pd
import ast
from ..data import parks_data, facilities_data, special_data, boundary_data
from ..components.map import create_markers, geo_location_dict

@callback(
    Output("vancouver-map", "children"),
    Output("vancouver-map", "viewport"),
    Output("num-parks-text", "children"),
    Output("avg-hectare-text", "children"),
    Input("neighbourhood-dropdown", "value"),
    Input("facility-dropdown", "value"),
    Input("special-feature-dropdown", "value"),
    Input("washrooms-checkbox", "value")
)
def update_map(selected_neighbourhood, selected_facilities, selected_special_features, washroom_filter):
    df_filtered = parks_data.copy()
    
    # Default center and zoom
    center = [49.2827, -123.1207]  # Default center (Vancouver)
    zoom = 12  # Default zoom level

    # Filter by neighbourhood
    if selected_neighbourhood:
        df_filtered = df_filtered[df_filtered["NeighbourhoodName"] == selected_neighbourhood]
        if selected_neighbourhood in geo_location_dict:
            center = geo_location_dict[selected_neighbourhood]['center']
            zoom = geo_location_dict[selected_neighbourhood]['zoom']

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

    # Apply the final filter
    df_filtered = df_filtered[df_filtered["ParkID"].isin(park_ids)]

    num_parks_filtered = df_filtered["ParkID"].nunique()
    avg_hectare_filtered = df_filtered["Hectare"].mean()

    num_parks_text = str(num_parks_filtered) if num_parks_filtered > 0 else "0"
    avg_hectare_text = f"{avg_hectare_filtered:.2f}" if not df_filtered.empty else "0.00"

    boundary_data_index = {
        'Arbutus-Ridge': 14,
        'Downtown': 0,
        'Dunbar-Southlands': 9,
        'Fairview': 10,
        'Grandview-Woodland': 15,
        'Hastings-Sunrise': 1,
        'Kensington-Cedar Cottage': 16,
        'Kerrisdale': 2,
        'Killarney': 17,
        'Kitsilano': 18,
        'Marpole': 3,
        'Mount Pleasant': 11,
        'Oakridge': 4,
        'Renfrew-Collingwood': 12,
        'Riley Park': 5,
        'Shaughnessy': 7,
        'South Cambie': 6,
        'Strathcona': 19,
        'Sunset': 20,
        'Victoria-Fraserview': 8,
        'West End': 13,
        'West Point Grey': 21
    }

    if selected_neighbourhood:
        filter_index = boundary_data_index.get(selected_neighbourhood)
        filtered_boundary = boundary_data.copy()
        filtered_boundary["features"] = [filtered_boundary["features"][filter_index]]
        print(filtered_boundary)

        result = ([dl.TileLayer(), dl.GeoJSON(data=filtered_boundary, style={"color": "red", "weight": 2, "fillOpacity": 0.2})] +
        create_markers(df_filtered),
        {"center": center, "zoom": zoom, "transition": "flyTo"},
        num_parks_text,
        avg_hectare_text,
        )
    else:
        result = ([dl.TileLayer()]+
        create_markers(df_filtered),
        {"center": center, "zoom": zoom, "transition": "flyTo"},
        num_parks_text,
        avg_hectare_text)


    return result