import streamlit as st
from datetime import datetime, timedelta

from src import load_places, load_GFS_analysis, image_rectangle, crop_image, load_GFS_anomaly

today = datetime.today()
last_week = today - timedelta(days=7)
last_2weeks = today - timedelta(days=14)

st.sidebar.page_link('main.py', label='HOME')
st.sidebar.page_link('pages/weather_map.py', label='WEATHER')
st.sidebar.page_link('pages/crop_map.py', label='CROP')

tab1, tab2, tab3 = st.tabs(['GFS Analysis', 'Color detection', '...'])

def_url = 'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_us_metric_2440.png'

with tab1:
    st.write('')
    col1, col2, col3 = st.columns([7.5,0.5,2])
    col3.markdown('**Selection**')
    sel_place = col3.selectbox('Region', key='tp1', options=load_places(), index=0)
    col1a, col2a = col3.columns([5,5])
    sel_date1 = col1a.date_input("Past date", key='tp2', value=last_week, format="YYYY-MM-DD",
                                 max_value=today, min_value=last_2weeks)
    sel_date2 = col2a.date_input("Current date", key='tp3', value=today, format="YYYY-MM-DD",
                                 max_value=today, min_value=last_2weeks)
    validate = col3.button('Show', key='tp4', use_container_width=True)

    if validate:
        st.write('')
        col1b, col2b, col3b = col1.columns([4.75,0.5,4.75])
        url1, url2, url3 = load_GFS_analysis(select_date=str(sel_date1), place=sel_place)
        url4, url5, url6 = load_GFS_analysis(select_date=str(sel_date2), place=sel_place)
        col1b.markdown(f"<h5 style='text-align: center; color: #8C7F3E;'>{sel_date1}</h1>", unsafe_allow_html=True)
        col1b.image(url2, use_column_width=True)
        col1b.image(url3, use_column_width=True)
        col1b.image(url1, use_column_width=True)
        col3b.markdown(f"<h5 style='text-align: center; color: #8C7F3E;'>{sel_date2}</h1>", unsafe_allow_html=True)
        col3b.image(url5, use_column_width=True)
        col3b.image(url6, use_column_width=True)
        col3b.image(url4, use_column_width=True)


with tab2:
    st.write('')
    col1, col2, col3 = st.columns([7.5,0.5,2])
    
    sel_place = col3.selectbox('Region', key='co0', options=load_places(), index=0)
    col1a, col2a = col3.columns([5,5])
    sel_date1 = col1a.date_input("Start date", key='co1', value=last_week, format="YYYY-MM-DD",
                                 max_value=today)
    sel_date2 = col2a.date_input("End date", key='co2', value=today, format="YYYY-MM-DD",
                                 max_value=today)
    col3.write('')
    with col3.expander('Crop coordinates'):
        top = st.number_input('Top corner', key='top', step=1, min_value=1, value=202)
        left = st.number_input('Left corner', key='left', step=1, min_value=1, value=242)
        bottom = st.number_input('Bottom corner', key='bottom', step=1, min_value=1, value=242)
        right = st.number_input('Right corner', key='Right', step=1, min_value=1, value=312)
        shape = st.selectbox('Shape', options=['rectangle', 'ellipse'], index=0)

    col3.write('')
    validate = col3.button('Show and crop', key='co5', use_container_width=True)

    if validate:
        col1.write('')
        col1a, col2a, col3a = col1.columns([6.75,0.5,2.75])
        url1 = load_GFS_anomaly(select_date=str(sel_date1), place=sel_place)
        img1 = image_rectangle(url=url1, left=left, top=top, right=right, bottom=bottom, forme=shape)
        col1a.image(img1)

        im_crop, color_ref = crop_image(url=def_url,
                        left=left, top=top, right=right, bottom=bottom,
                        )
        col3a.image(im_crop)
        col3a.write(color_ref)
