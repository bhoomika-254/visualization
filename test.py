import streamlit as st
import visualization_window
import webbrowser
import base64
import map_api_window
import no2visualization_window
from air_quality_prediction import lstm_windoww
import nearest_station_window
import home 
from ndvi import ndvi_window
import chatbot_window

# Set page configuration (must be the first Streamlit command)
st.set_page_config(layout="wide", page_title="Air Quality Dashboard", page_icon="🌍")

st.markdown(
    """
    <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.1); /* Translucent white background */
            backdrop-filter: blur(10px); /* Glass effect */
            -webkit-backdrop-filter: blur(10px); /* Glass effect for Safari */
            border-right: 1px solid rgba(255, 255, 255, 0.2); /* Subtle border */
        }

        /* Sidebar text styling */
        [data-testid="stSidebar"] .css-1d391kg { 
            color: #333; /* Dark text for readability */
        }

        /* Adjust scrollbar for sidebar */
        [data-testid="stSidebar"]::-webkit-scrollbar {
            width: 8px;
        }

        [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
        }

        /* Sidebar header text style */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #FFFFFF; /* Soft blue for headings */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for navigation
st.sidebar.title("Navigation")
# Sidebar for navigation using radio buttons
page = st.sidebar.radio("Go to", [
    "Home",
    "Visualization Hub", 
    "Prediction Models", 
    "Latitude and Longitude", 
    "Find Nearest Station",
    "Air Quality Assistant",
    "NO2 Insights",
    "NDVI Section"
])

# ---------------------------------------------------- linking pages ------------------------------------------------

if page=="Home":
    home.show_page()
elif page == "Visualization Hub":
    visualization_window.show_page()
elif page == "Prediction Models":
    lstm_windoww.show_page()
elif page == "NO2 Insights":
    no2visualization_window.show_page()
elif page == "Air Quality Assistant":
    chatbot_window.show_page()
elif page == "Latitude and Longitude":
    map_api_window.show_page()
elif page == "Find Nearest Station":
    nearest_station_window.show_page()
elif page == "NDVI Section":
    ndvi_window.show_page()
    
     
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
