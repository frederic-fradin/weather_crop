import streamlit as st
from datetime import datetime

today = datetime.today()
current_year = today.year

# Page configuration
st.set_page_config(
    page_title="Crop Weather",
    page_icon="🌤️",
    layout = 'wide'
    )

# Page header
col1, col2, col3 = st.columns([0.55, 0.10, 0.35])
col1.title("Weather analysis for crop production")
col3.image('./reports/figures/main_img.jpg')
col1.write('Data from World Ag Weather (https://www.worldagweather.com/)')