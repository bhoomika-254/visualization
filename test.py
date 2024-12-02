import streamlit as st
import visualization_window
import webbrowser
import base64
import map_api_window
import no2visualization
from air_quality_prediction import lstm_window
import nearest_station_window

# Set page configuration (must be the first Streamlit command)
st.set_page_config(layout="wide", page_title="Air Quality Dashboard", page_icon="🌍")

# Sidebar for navigation
st.sidebar.title("Navigation")
# Sidebar for navigation using radio buttons
page = st.sidebar.radio("Go to", [
    "Visualization Hub", 
    "Prediction Models", 
    "API using Lat Long", 
    "Find Nearest Station",
    "Air Quality Assistant",
    "NO2 Insights"
])

# ---------------------------------------------------- linking pages ------------------------------------------------

if page == "Visualization Hub":
    visualization_window.show_page()
elif page == "Prediction Models":
    lstm_window.show_page()
elif page == "NO2 Insights":
    no2visualization.show_page()
elif page == "Air Quality Assistant":
    webbrowser.open("https://yaksha.streamlit.app/")
elif page == "API using Lat Long":
    map_api_window.show_page()
elif page == "Find Nearest Station":
    nearest_station_window.show_page()
     
# ------------------------------------------------------ background -------------------------------------------------------

# Function to load and encode image as base64
# def get_base64_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# # Load the background image (adjust the path to your image)
# background_image_path = './bg.jpg'  # Replace with your image path
# background_image_base64 = get_base64_image(background_image_path)

# # Set up the CSS for the background
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/png;base64,{background_image_base64});
#         background-size: cover;  /* Cover the entire background */
#         background-position: center; /* Center the image */
#         background-repeat: no-repeat; /* Prevent repeating */
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )
