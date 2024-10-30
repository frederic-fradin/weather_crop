import os
import streamlit as st
import pandas as pd
from datetime import datetime, date

directory = os.path.dirname(os.path.abspath(__file__))

from src import load_crop_calendar

st.sidebar.page_link('main.py', label='HOME')
st.sidebar.page_link('pages/weather_map.py', label='WEATHER')
st.sidebar.page_link('pages/crop_map.py', label='CROP')

tab1, tab2, tab3 = st.tabs(['Crop calendar', '...', '...'])

data, region, product = load_crop_calendar()

dict_month = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6,
              'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}

today = datetime.today()
month_str = today.strftime("%B")
month_id = dict_month[month_str[:3].upper()] -1

with tab1:
    st.write('')
    col1, col2, col3 = st.columns([7.5,0.5,2])
    sel_product = col3.multiselect('Product', key='cr1', options=product, default=['WHEAT', 'CORN'])
    sel_region = col3.multiselect('Region', key='cr2', options=region, default=['Europe', 'West Asia'])
    sel_month = col3.selectbox('First month', key='cr3', options=dict_month.keys(), index=month_id)
    col3.write('')
    validate = col3.button('Show', key='cr4', use_container_width=True)

    if validate:
        base_month = dict_month[sel_month]
        min_col = base_month + 3
        max_col = base_month + 15
        first_columns = data.iloc[:, :4]
        last_columns = data.iloc[:, min_col:max_col]
        select = pd.concat([first_columns, last_columns], axis=1)
        
        select = select.fillna('')
        select = select[(select['REGION'].isin(sel_region)) & (select['PRODUCTION'].isin(sel_product))].copy()
        
        def color_vowel(value):
            color = (f"background-color: #6B8C4A; color: #2E4022" if value in ["PLA"]
                     else f"background-color: #D9B343; color: #8C7F3E;" if value in ["HAR"]
                     else None)
            return color
        
        select_df = select.drop(columns=['REGION'])
        list_col = select_df.columns.to_list()
        col1.write('Source USDA : (PLA) Plant - (HAR) Harvest - (FLO) Flowering')
        col1.dataframe(select_df.style.map(color_vowel, subset=list_col),
                       hide_index=True, use_container_width=True)
        
        short_month = sel_month.lower()
        file_path = os.path.join(directory, f'../reports/figures/{short_month[:3]}_calendar.gif')
        col1.write('')
        col1.write('')
        col1.image(file_path, use_column_width=True)

        # Ajouter affichage commentaire si selection colonne avec info sur point d'alerte crop selon USDA
        # https://ipad.fas.usda.gov/ogamaps/cropmapsandcalendars.aspx

        
