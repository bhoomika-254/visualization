import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from heatmap_module import create_heatmap
from streamlit_folium import st_folium
from streamlit_globe import streamlit_globe
import random
import base64

st.set_page_config(layout="wide")

# File paths
GROUND_DATA_PATH = "ground_data2.csv"
SATELLITE_DATA_PATH = "satellite_data2.csv"

# Load data
data = pd.read_csv(GROUND_DATA_PATH)
satellite_data = pd.read_csv(SATELLITE_DATA_PATH)

# Ensure correct data types
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y %H:%M', errors='coerce')
for col in data.columns:
    if col not in ['Date', 'City', 'Location', 'Latitude', 'Longitude']:
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Clean Latitude and Longitude columns
data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')

# Remove rows with invalid Latitude/Longitude
data = data.dropna(subset=['Latitude', 'Longitude'])

st.title("Visualization Window")
col1, col2 = st.columns([1, 2])

# Sidebar Filters
with col1:
    city = st.selectbox('Select City', data['City'].unique(), key="city_select")
    data_type = st.radio("Select Type of Data for Visualization :", ['Ground Data', 'Satellite Data'], key="heatmap_data_type")
    locations = data[data['City'] == city]['Location'].unique().tolist()
    locations.append('Select All Locations')
    selected_locations = st.multiselect('Select Locations', locations, key="location_select")
    city_data = data[data['City'] == city]
    if 'Select All Locations' not in selected_locations:
        city_data = city_data[city_data['Location'].isin(selected_locations)]
    pollutants = [col for col in city_data.columns if col not in ['Date', 'City', 'Location', 'Latitude', 'Longitude']]
    selected_pollutants = st.multiselect('Select Pollutants', pollutants, key="pollutant_select")

with col2:
    # Generate points data with random AQI values and unique colors
    pointsData = [
        {'lat': 28.7041, 'lng': 77.1025, 'size': 0.01, 'color': 'red'},  # Delhi
        {'lat': 19.0760, 'lng': 72.8777, 'size': 0.01, 'color': 'blue'},  # Mumbai
        {'lat': 13.0827, 'lng': 80.2707, 'size': 0.01, 'color': 'green'},  # Chennai
        {'lat': 22.5726, 'lng': 88.3639, 'size': 0.01, 'color': 'orange'},  # Kolkata
        {'lat': 12.9716, 'lng': 77.5946, 'size': 0.01, 'color': 'purple'},  # Bengaluru
        {'lat': 17.3850, 'lng': 78.4867, 'size': 0.01, 'color': 'yellow'},  # Hyderabad
        {'lat': 26.9124, 'lng': 75.7873, 'size': 0.01, 'color': 'pink'},  # Jaipur
        {'lat': 21.1702, 'lng': 72.8311, 'size': 0.01, 'color': 'cyan'},  # Surat
        {'lat': 18.5204, 'lng': 73.8567, 'size': 0.01, 'color': 'magenta'},  # Pune
        {'lat': 23.0225, 'lng': 72.5714, 'size': 0.01, 'color': 'lime'},  # Ahmedabad
        {'lat': 30.7333, 'lng': 76.7794, 'size': 0.01, 'color': 'teal'},  # Chandigarh
        {'lat': 11.0168, 'lng': 76.9558, 'size': 0.01, 'color': 'gold'},  # Coimbatore
        {'lat': 31.1048, 'lng': 77.1734, 'size': 0.01, 'color': 'brown'},  # Shimla
        {'lat': 25.5941, 'lng': 85.1376, 'size': 0.01, 'color': 'olive'},  # Patna
        {'lat': 19.9975, 'lng': 73.7898, 'size': 0.01, 'color': 'navy'},  # Nashik
        {'lat': 22.3072, 'lng': 73.1812, 'size': 0.01, 'color': 'violet'},  # Vadodara
        {'lat': 34.0837, 'lng': 74.7973, 'size': 0.01, 'color': 'coral'},  # Srinagar
        {'lat': 15.3173, 'lng': 75.7139, 'size': 0.01, 'color': 'maroon'},  # Hampi
        {'lat': 27.1767, 'lng': 78.0081, 'size': 0.01, 'color': 'crimson'},  # Agra
        {'lat': 24.5854, 'lng': 73.7125, 'size': 0.01, 'color': 'indigo'}   # Udaipur
    ]

    # Add labels with city name and AQI value
    labelsData = [
        {
            'lat': location['lat'],
            'lng': location['lng'],
            'size': location['size'],
            'color': location['color'],
            'text': f"{name} (AQI: {location['size']:.2f})"
        } for location, name in zip(pointsData, [
            'Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bengaluru', 'Hyderabad', 'Jaipur', 'Surat', 'Pune', 'Ahmedabad',
            'Chandigarh', 'Coimbatore', 'Shimla', 'Patna', 'Nashik', 'Vadodara', 'Srinagar', 'Hampi', 'Agra', 'Udaipur'
        ])
    ]

    # Render the globe
    streamlit_globe(pointsData=pointsData, labelsData=labelsData, daytime='day', width=800, height=600)

col3, col4 = st.columns([1, 1])
# Heatmap Display
with col3:
    if data_type == 'Ground Data' and city_data is not None and not city_data.empty:
        pollutant = 'NO2'  # Default pollutant for heatmap

        # Debug center coordinates
        center_lat = city_data['Latitude'].mean()
        center_lon = city_data['Longitude'].mean()
        st.subheader("NO2 Heatmap :")
        if pd.notnull(center_lat) and pd.notnull(center_lon):
            heatmap = create_heatmap(data_type, center_lat, center_lon, pollutant=pollutant)
            st_folium(heatmap, width=700, height=500)
        else:
            st.error("Invalid coordinates for the selected city or locations.")

    elif data_type == 'Satellite Data':
        data_file = SATELLITE_DATA_PATH
        pollutant = 'NO2'  # Default pollutant for heatmap
    
        st.subheader(f"Satellite Data Analysis for {city}")
        # Debug center coordinates
    
        try:
            # Compute center coordinates
            center_lat = city_data['Latitude'].mean()
            center_lon = city_data['Longitude'].mean()
    
            if pd.notnull(center_lat) and pd.notnull(center_lon):
                st.subheader("NO2 Heatmap :")
                heatmap = create_heatmap(data_type, center_lat, center_lon, pollutant=pollutant)
                st_folium(heatmap, width=700, height=500)
            else:
                st.error("Invalid coordinates for the selected city or locations. Please check the data.")
        except KeyError as e:
            st.error(f"Missing required column in satellite data: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")


# -----------------------------------------------------------------      VISUALIZAATIONS      -------------------------------------------------------------------------------------------

# Air quality chart
if selected_pollutants:
    with col4:
        st.subheader(f"Air Quality Analysis in {city} : ")
        if not city_data['Date'].isnull().all():
            year = city_data['Date'].dt.year.unique()[0]
            st.markdown(f"**Year:** {year}")

            # Line Chart
            # Add a column for formatted dates in the desired format
            city_data['Formatted_Date'] = city_data['Date'].apply(
                lambda x: f"{x.day}{'th' if 11 <= x.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(x.day % 10, 'th')} {x.strftime('%b')}"
            )

            # Sort data by date
            # Sort data by date
            city_data.sort_values('Date', inplace=True)

            # Select indices for 7-day intervals
            seven_day_indices = range(0, len(city_data), 7)

            with plt.style.context('dark_background'):
                fig, ax = plt.subplots(figsize=(10, 6))
                colors = sns.color_palette("bright", len(selected_pollutants))

                # Plot each pollutant with all data points
                for i, pollutant in enumerate(selected_pollutants):
                    city_data[pollutant].fillna(method='bfill', inplace=True)
                    ax.plot(city_data['Formatted_Date'], city_data[pollutant], label=f'{pollutant}', color=colors[i])

                # Set x-ticks and labels only for 7-day intervals
                ax.set_xticks([city_data['Formatted_Date'].iloc[i] for i in seven_day_indices])
                ax.set_xticklabels([city_data['Formatted_Date'].iloc[i] for i in seven_day_indices], 
                                rotation=45, ha='right', fontsize=8)

                ax.legend(loc='upper center', ncol=len(selected_pollutants), fontsize=8)
                ax.set_xlabel("Date", fontsize=10)
                ax.set_ylabel("Pollutant Levels", fontsize=10)
                ax.set_title("Pollutant Trends Over Two Months", fontsize=12)
                st.pyplot(fig)

    # Define gauge metrics
    # Define a color palette for pollutants
# Assuming `city_data` and `selected_pollutants` are already defined
    col5, col6 = st.columns([2, 2])

# Define gauge metrics
    color_palette = {
            "NO2": "red",
            "PM2.5": "orange",
            "PM10": "yellow",
            "Ozone": "blue",
            "SO2": "green",
            "CO": "purple",
            "NO": "pink",
            "NOx": "brown",
    }

    # Define gauge metrics
    gauge_metrics = {
        "NO2": (city_data['NO2'].mean(), 0, 200),
        "PM2.5": (city_data['PM2.5'].mean(), 0, 150),
        "PM10": (city_data['PM10'].mean(), 0, 250),
        "Ozone": (city_data['Ozone'].mean(), 0, 180),
        "SO2": (city_data['SO2'].mean(), 0, 100),
        "CO": (city_data['CO'].mean(), 0, 10),
        "NO": (city_data['NO'].mean(), 0, 100),
        "NOx": (city_data['NOx'].mean(), 0, 150),
    }

    # Render gauge charts
    # st.subheader("Gauge Charts: Pollutant Levels")

    # # Maximum number of columns for the layout
    # max_cols = 4  

    # # Total number of pollutants selected
    # total_charts = len(selected_pollutants)

    # # Dynamically calculate rows
    # rows = (total_charts + max_cols - 1) // max_cols

    # # Adjust gauge chart size to fit more charts in limited space
    # chart_height = 200  # Reduced height for better fit

    # for row in range(rows):
    #     # Create dynamic columns for the current row
    #     cols = st.columns(max_cols if row < rows - 1 else total_charts % max_cols or max_cols)
        
    #     for idx, col in enumerate(cols):
    #         chart_idx = row * max_cols + idx
    #         if chart_idx < total_charts:
    #             pollutant = selected_pollutants[chart_idx]
    #             if pollutant in gauge_metrics:
    #                 value, min_value, max_value = gauge_metrics[pollutant]
    #                 if pd.notnull(value):
    #                     # Create gauge chart
    #                     fig = go.Figure(go.Indicator(
    #                         mode="gauge+number",
    #                         value=value,
    #                         title={'text': pollutant, 'font': {'size': 12}},  # Reduced font size
    #                         gauge={
    #                             'axis': {'range': [min_value, max_value]},
    #                             'bar': {'color': "blue"},
    #                             'steps': [
    #                                 {'range': [min_value, max_value * 0.5], 'color': "lightgray"},
    #                                 {'range': [max_value * 0.5, max_value], 'color': "lightblue"}
    #                             ],
    #                             'threshold': {
    #                                 'line': {'color': "red", 'width': 3},  # Reduced threshold line width
    #                                 'thickness': 0.5,
    #                                 'value': value * 0.9 if value * 0.9 < max_value else max_value
    #                             }
    #                         }
    #                     ))
    #                     # Display chart in the current column
    #                     col.plotly_chart(fig, use_container_width=True, height=chart_height)

    st.subheader("Gauge Charts: Pollutant Levels")

    # Maximum number of columns for the layout
    max_cols = 4  

    # Total number of pollutants selected
    total_charts = len(selected_pollutants)

    # Adjust gauge chart size to fit more charts in limited space
    chart_height = 200  # Reduced height for better fit

    # Iterate through the pollutants in groups of max_cols
    for i in range(0, total_charts, max_cols):
        cols = st.columns(max_cols)  # Create exactly `max_cols` columns for each row
        
        # Iterate through pollutants in the current group
        for j, col in enumerate(cols):
            idx = i + j  # Calculate the index of the pollutant
            if idx < total_charts:
                pollutant = selected_pollutants[idx]
                if pollutant in gauge_metrics:
                    value, min_value, max_value = gauge_metrics[pollutant]
                    if pd.notnull(value):
                        # Create gauge chart
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=value,
                            title={'text': pollutant, 'font': {'size': 12}},  # Reduced font size
                            gauge={
                                'axis': {'range': [min_value, max_value]},
                                'bar': {'color': "blue"},
                                'steps': [
                                    {'range': [min_value, max_value * 0.5], 'color': "lightgray"},
                                    {'range': [max_value * 0.5, max_value], 'color': "lightblue"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 2},  # Reduced threshold line width
                                    'thickness': 0.5,
                                    'value': value * 0.9 if value * 0.9 < max_value else max_value
                                }
                            }
                        ))
                        # Display chart in the current column
                        col.plotly_chart(fig, use_container_width=True, height=chart_height)



    # Bar Chart
    with col5:
        st.subheader("Bar Chart: Over the Last 30 Days")
        recent_data = city_data.tail(30)

        if selected_pollutants:
            fig = px.bar(
                recent_data,
                x=recent_data['Date'].dt.strftime('%d-%b'),
                y=selected_pollutants,
                barmode='group',
                title="Pollutant Levels Over the Last 30 Days",
                labels={'value': 'Concentration', 'Date': 'Date'},
                height=500
            )
            st.plotly_chart(fig)
              
    # Pie Chart
    with col6:
        if len(selected_pollutants) > 1:
            st.subheader("Pie Chart: Pollutant Breakdown")
            pollutant_data = city_data[selected_pollutants].mean()
            fig = px.pie(
                values=pollutant_data,
                    names=pollutant_data.index,
                    title="Pollutant Contribution",
                    hole=0
            )
            st.plotly_chart(fig)
        
    st.subheader("Histogram: ")
            # Group data by Date and calculate the mean NO2 per day
    grouped_data = city_data.groupby('Date', as_index=False)['NO2'].mean()

            # Create the histogram
    fig = px.histogram(
                grouped_data,
                x='Date',
                y='NO2',
                nbins=20,
                title="Date vs NO2 Distribution",
                color_discrete_sequence=['#7e3bec']  # Change color to purple
    )

            # Update layout for better aesthetics
    fig.update_layout(
                xaxis_title="Date",
                yaxis_title="NO2 Concentration",
                template="plotly_white",
    )

            # Render the histogram
    st.plotly_chart(fig)

    #3D Scatter Plot
    st.subheader("3D Scatter Plot:")

    if len(selected_pollutants) >= 3:
            # Select pollutants for x, y, and z axes
        x_pollutant = st.selectbox('Select x-axis pollutant', selected_pollutants, key="x_pollutant_select")
        y_pollutant = st.selectbox('Select y-axis pollutant', selected_pollutants, key="y_pollutant_select")
        z_pollutant = st.selectbox('Select z-axis pollutant', selected_pollutants, key="z_pollutant_select")
                
            # Convert z_pollutant to a categorical type for distinct colors
        filtered_data = city_data.dropna(subset=[x_pollutant, y_pollutant, z_pollutant])
        filtered_data[z_pollutant] = filtered_data[z_pollutant].astype(str)
                
            # Define a qualitative color palette
        color_palette = px.colors.qualitative.Set1  # Distinct color palette
                
            # Create the 3D scatter plot
        fig = px.scatter_3d(
                filtered_data,
                x=x_pollutant,
                y=y_pollutant,
                z=z_pollutant,
                color=z_pollutant,  # Now z_pollutant is treated as categorical
                color_discrete_sequence=color_palette
        )
                
            # Render the plot
        st.plotly_chart(fig)
#setting background

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('bg.png')
