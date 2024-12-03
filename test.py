import streamlit as st
import visualization_window
import webbrowser
import base64
import map_api_window
import no2visualization

# Set page configuration (must be the first Streamlit command)
st.set_page_config(layout="wide", page_title="Air Quality Dashboard", page_icon="🌍")

# Sidebar for navigation
st.sidebar.title("Navigation")
# Sidebar for navigation using radio buttons
page = st.sidebar.radio("Go to", [
    "Visualization Window", 
    "LSTM Window", 
    "API using Lat Long", 
    "Nearest Station Prediction",
    "Clustering Window",
    "Chat Bot",
    "NO2 Visualization"
])

# ---------------------------------------------------- linking pages ------------------------------------------------

if page == "Visualization Window":
    visualization_window.show_page()
elif page == "LSTM Window":
    webbrowser.open("https://air-quality-pavanai.streamlit.app/")
elif page == "NO2 Visualization":
    no2visualization.show_page()
elif page == "Chat Bot":
    webbrowser.open("https://yaksha.streamlit.app/")
elif page == "API using Lat Long":
    map_api_window.show_page()
elif page == "Nearest Station Prediction":
    st.header("Predicting the nearest station here - ")
elif page == "Clustering Window":
    st.header("Clustering Window - ")
