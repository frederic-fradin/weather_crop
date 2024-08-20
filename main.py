import streamlit as st
from datetime import datetime

today = datetime.today()
current_year = today.year

# Page configuration
st.set_page_config(
    page_title="Crop Weather",
    page_icon="🌤️",
    layout = 'wide',
    initial_sidebar_state="expanded"
    )

# Adjust top padding
st.markdown("""
            <style>
                    .block-container {
                        padding-top: 4rem;
                        padding-bottom: 4rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """, unsafe_allow_html=True)

st.sidebar.page_link('main.py', label='HOME')
st.sidebar.page_link('pages/weather_map.py', label='WEATHER')
st.sidebar.page_link('pages/crop_map.py', label='CROP')

# Page header
col1, col2, col3 = st.columns([0.55, 0.10, 0.35])
col1.title("Weather analysis for crop production")
col3.image('./reports/figures/main_img.jpg')
col1.write('Data from World Ag Weather (https://www.worldagweather.com/)')