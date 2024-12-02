import folium
import pandas as pd
from folium.plugins import HeatMap
import numpy as np

# Define file paths for different data types
DATA_TYPE_PATHS = {
    "Ground Data": "ground_data2.csv",
    "Satellite Data": "satellite_data2.csv",
    # Add more data types and their paths if needed
}

def create_heatmap(data_type, center_lat, center_lon, pollutant='NO2', zoom_start=10):
    """
    Generate a heatmap based on pollutant concentration.

    Args:
        data_type (str): Type of data to use ('Ground Data', 'Satellite Data', etc.).
        center_lat (float): Latitude for the initial map center.
        center_lon (float): Longitude for the initial map center.
        pollutant (str): Pollutant to visualize (e.g., NO2).
        zoom_start (int): Initial zoom level for the map.

    Returns:
        folium.Map: A folium map object with the heatmap overlay.
    """
    # Select the appropriate data file based on the data type
    data_file = DATA_TYPE_PATHS.get(data_type)
    if not data_file:
        raise ValueError(f"Unknown data type '{data_type}'. Please provide a valid data type.")

    # Load the data
    try:
        data = pd.read_csv(data_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file for '{data_type}' not found at path: {data_file}")

    # Filter and clean data
    if pollutant not in data.columns:
        raise ValueError(f"{pollutant} is not present in the data columns.")

    # Clean Latitude, Longitude, and Pollutant columns
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
    data[pollutant] = pd.to_numeric(data[pollutant], errors='coerce')

    # Drop rows with invalid values
    data = data.dropna(subset=['Latitude', 'Longitude', pollutant])

    # Convert to heatmap data format
    heatmap_data = data[['Latitude', 'Longitude', pollutant]].values.tolist()

    if not heatmap_data:
        raise ValueError("No valid data points available to generate a heatmap.")

    # Create a folium map centered at the given latitude and longitude
    folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)

    # Add heatmap overlay
    HeatMap(heatmap_data, radius=15, max_zoom=10).add_to(folium_map)

    return folium_map
