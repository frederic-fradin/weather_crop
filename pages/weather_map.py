import streamlit as st
from datetime import datetime, timedelta
import json
import os

directory = os.path.dirname(os.path.abspath(__file__))

from src import load_places, load_GFS_analysis, image_rectangle, crop_image, get_size

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
    
    file_path = os.path.join(directory, '../data/processed/coord_dict.json')
    try:
        coord_dict = json.load(open(file_path))
    except:
        coord_dict = {}

    col3.write('')
    with col3.expander('Crop coordinates'):
        w, h = get_size(def_url)
        params = st.selectbox(label='Favorites', options=coord_dict.keys(), index=None)
        if params:
            fav = coord_dict[params]
            x1, x2 = fav[0][0], fav[0][1]
            y1, y2 = fav[1][0], fav[1][1]
        else:
            x1, x2 = 0, w
            y1, y2 = 0, h

        x_values = st.slider("Select X range", 0, int(w), (x1, x2), step=2)
        y_values = st.slider("Select Y range", 0, int(h), (y1, y2), step=2)
        shape = st.selectbox('Shape', options=['rectangle', 'ellipse'], index=0)
        name = st.text_input("Name", "default")
        save = st.button(label="Save", use_container_width=True)

        if save:
            coord_dict[name] = [x_values, y_values]
            json.dump(coord_dict, open(file_path, 'w'))

    
    col1a, col2a, col3a = col1.columns([4.8, 0.4, 4.8])
    img1 = image_rectangle(url=def_url, left=int(x_values[0]), top=int(y_values[0]),
                           right=int(x_values[1]), bottom=int(y_values[1]), forme=shape)
    
    col1a.write('')
    col1a.image(img1)
    validate = col3.button('Show and crop', key='co5', use_container_width=True)

    if validate:
        # url1 = load_GFS_anomaly(select_date=str(sel_date1), place=sel_place)

        im_crop, image_dict, fig, fig2 = crop_image(url=def_url, left=int(x_values[0]), top=int(y_values[0]),
                           right=int(x_values[1]), bottom=int(y_values[1]),
                        )
        
        col3a.plotly_chart(fig)
        col1.plotly_chart(fig2)
