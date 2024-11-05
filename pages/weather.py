import streamlit as st
import json
import pandas as pd
import os

from datetime import datetime, timedelta
from src import load_places, load_GFS_analysis, load_crop_analysis, load_crop_calendar
from src import add_rectangle, crop_image, get_size, generate_date_serie, create_chart

directory = os.path.dirname(os.path.abspath(__file__))
file_json = os.path.join(directory, '../data/processed/coord_dict.json')

today = datetime.today()
last_week = today - timedelta(days=7)
last_2weeks = today - timedelta(days=14)
last_quarter = today - timedelta(days=90)
month_str = today.strftime("%B")

data, region, product = load_crop_calendar()
product_list = [x.capitalize() for x in product]
dict_month = {1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}


tab1, tab2, tab3 = st.tabs(['WEATHER', '...', '...'])

with tab1:
    # Main filters
    col1, col2, col3, col4, col5 = st.columns([2,2,2,2,2])
    sel_place = col1.selectbox('Region', key='tp1', options=load_places(), index=0)
    sel_date1 = col2.date_input("Date", key='tp2', value=today, format="YYYY-MM-DD", max_value=today)
    sel_product = col3.selectbox('Product', key='tp3', options=product_list, index=0)

    with st.expander(f'GFS Situation'):
        st.write('')
        col1b, col2b, col3b = st.columns([4.75,0.5,4.75])

        url1, url2, url3, url4 = load_GFS_analysis(select_date=str(sel_date1), place=sel_place)
        col1b.image(url1, use_column_width=True)
        col3b.image(url2, use_column_width=True)
        col1b.image(url3, use_column_width=True)
        col3b.image(url4, use_column_width=True)

        col1b.divider()
        col3b.divider()

        url5, url6, url7, url8 = load_crop_analysis(select_date=str(sel_date1), place=sel_place)
        col3b.image(url7, use_column_width=True)
        col1b.image(url8, use_column_width=True)
        col3b.image(url5, use_column_width=True)
        col1b.image(url6, use_column_width=True)


    with st.expander(f'GFS Analysis'):
        st.write('')
        col1, col2, col3 = st.columns([7.5,0.5,2])
        url1, url2, url3, url4 = load_GFS_analysis(select_date=str(sel_date1), place=sel_place)
        col3.write('')
        sel_date2 = col3.date_input("Start date", key='co2', value=last_quarter, format="YYYY-MM-DD", max_value=sel_date1)

        def save_json(content):
            with open(file_json, "w") as outfile: 
                    json.dump(content, outfile)

        try:
            with open(file_json , "r") as json_file:
                file_data = json.load(json_file)
        except:
            file_data = {}

        @st.dialog("Save zoom")
        def save_zoom(x, y, w, h):
            zoom_name = st.text_input("Name the place")
            if st.button("Submit", use_container_width=True):
                file_data[zoom_name] = [x, y, w, h]
                save_json(file_data)
                
                st.rerun()

        sel_zoom = col3.selectbox('Zoom favorite', key='co3', options=file_data.keys(), index=None)
        if sel_zoom:
            x_def = file_data[sel_zoom][0]
            y_def = file_data[sel_zoom][1]
            w_def = file_data[sel_zoom][2]
            h_def = file_data[sel_zoom][3]
        else:
            x_def = 100
            y_def = 100
            w_def = 100
            h_def = 100

        with col3.popover('Focus coordinates', use_container_width=True):
            w, h = get_size(url1)
            x_values = st.slider("Select X position", 0, int(w), x_def, step=2)
            y_values = st.slider("Select Y position", 0, int(h), y_def, step=2)
            w_values = st.slider("Select width", 0, int(w), w_def, step=2)
            h_values = st.slider("Select height", 0, int(h), h_def, step=2)
            if st.button("Add favorite", use_container_width=True):
                save_zoom(x_values, y_values, w_values, h_values)

        img1 = add_rectangle(url=url1, left=int(x_values), top=int(y_values),
                        right=int(x_values + w_values), bottom=int(y_values + h_values))
            
        col1a, col2a, col3a = col1.columns([6, 0.2, 3.8])
        col1a.image(img1)
        validate2 = col3.button('Analyse', key='co5', use_container_width=True, type="primary")
        col3.write('')
        date_serie = generate_date_serie(sel_date2, sel_date1, 5)

        if validate2 and len(date_serie) !=0:
            hist = pd.DataFrame()

            # Loop through a serie of date
            # col1.write(date_serie)
            for d in date_serie:
                try:
                    url1s, url2s, url3s, url4s = load_GFS_analysis(select_date=str(d), place=sel_place)
                    im_crop, df = crop_image(url=url1s,
                                            left=int(x_values), top=int(y_values),
                                            right=int(x_values + w_values), bottom=int(y_values + h_values),
                                            date=d, place=sel_place)
                    
                    hist = pd.concat([df, hist], axis=0)
                except:
                    hist = hist

            # Store for result of each date in a dataframe
            fig1, fig2 = create_chart(hist)
            col3a.plotly_chart(fig1)
            col1.plotly_chart(fig2)

    with st.expander(f'Crop calendar'):
        st.write('')
        base_month = today.month
        min_col = base_month + 3
        max_col = base_month + 15
        first_columns = data.iloc[:, :4]
        last_columns = data.iloc[:, min_col:max_col]
        select = pd.concat([first_columns, last_columns], axis=1)
        
        select = select.fillna('')
        select = select[(select['REGION'].isin([sel_place])) & (select['PRODUCTION'].isin([sel_product.upper()]))].copy()

        def color_vowel(value):
            color = (f"background-color: #6B8C4A; color: #2E4022" if value in ["PLA"]
                     else f"background-color: #D9B343; color: #8C7F3E;" if value in ["HAR"]
                     else None)
            return color
        
        select_df = select.drop(columns=['REGION'])
        list_col = select_df.columns.to_list()
        st.write('Source USDA : (PLA) Plant - (HAR) Harvest - (FLO) Flowering')
        st.dataframe(select_df.style.map(color_vowel, subset=list_col),
                       hide_index=True, use_container_width=True)
        
        short_month = month_str.lower()
        file_path = os.path.join(directory, f'../reports/figures/{short_month[:3]}_calendar.gif')
        st.write('')
        st.write('')
        st.image(file_path, use_column_width=True)
        
        # Ajouter affichage commentaire si selection colonne avec info sur point d'alerte crop selon USDA
        # https://ipad.fas.usda.gov/ogamaps/cropmapsandcalendars.aspx