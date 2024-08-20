import os
import pandas as pd
import streamlit as st
from datetime import date, datetime

directory = os.path.dirname(os.path.abspath(__file__))

'''

Model GFS
Anomalies temperatures 1-7 jours :  https://www.worldagweather.com/fcstwx/tmp_gefs_day7_in_metric_2440.png
Precipitation 1-7 jours :           https://www.worldagweather.com/fcstwx/pcp_gfs_day7_in_metric_2440.png
Past anomalies 7 day total :        https://www.worldagweather.com/pastwx/pastpcp_in_7day_metric_4433.png

Map of production par product
https://ipad.fas.usda.gov/cropexplorer/cropview/commodityView.aspx?cropid=0440000


'''

dict_refid = {
    'tmp_gefs_day7':[2440, '2024-08-18'],
    'pcp_gfs_day7':[2441, '2024-08-18'],
    'pastpcp_in_7day':[4433, '2024-08-16'],
    }

dict_place = {
    'North America': 'na',
    'Europe':'eu',
    'South America (North)':'br',
    'South America (South)':'ar',
    'Central America':'ca',
    'West Asia':'wa',
    'East Asia':'cn',
    'Southeast Asia':'se',
    'Africa':'af',
    'Australia':'au',
    'India':'in',
    }

def load_places() -> list:
    list_place = []
    for key, value in dict_place.items():
        list_place.append(key)
    
    return list_place

def load_analysis() -> list:
    list_analysis = []
    for key, value in dict_refid.items():
        list_analysis.append(key)
    
    return list_analysis

def calculate_id_date(select_date:str, type:str) -> int:
    piv_id = dict_refid[type][0]
    piv_date = datetime.strptime(dict_refid[type][1], "%Y-%m-%d")
    sel_date = datetime.strptime(select_date, "%Y-%m-%d")

    # Calculate difference of days between 2 dates
    d0 = date(piv_date.year, piv_date.month, piv_date.day)
    d1 = date(sel_date.year, sel_date.month, sel_date.day)
    delta = d1 - d0
    sel_id = piv_id + delta.days

    return int(sel_id)

@st.cache_data
def load_GFS_analysis(select_date:str, place:str) -> object:
    id_place = dict_place[place]

    id1 = calculate_id_date(select_date, type='tmp_gefs_day7')
    url1 = f'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_{id_place}_metric_{id1}.png'

    id2 = calculate_id_date(select_date, type='pcp_gfs_day7')
    url2 = f'https://www.worldagweather.com/fcstwx/pcp_gfs_day7_{id_place}_metric_{id2}.png'

    id3 = calculate_id_date(select_date, type='pastpcp_in_7day') - 2
    url3 = f'https://www.worldagweather.com/pastwx/pastpcp_{id_place}_7day_metric_{id3}.png'

    return url3, url2, url1

@st.cache_data
def load_GFS_anomaly(select_date:str, place:str) -> object:
    id_place = dict_place[place]

    id1 = calculate_id_date(select_date, type='tmp_gefs_day7')
    url1 = f'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_{id_place}_metric_{id1}.png'

    return url1

def load_crop_calendar():
    file_path = os.path.join(directory, '../data/processed/crop_calendar.xlsx')
    data = pd.read_excel(file_path, sheet_name='Feuil1')

    region = data['REGION'].unique()
    product = data['PRODUCTION'].unique()

    return data, region, product

if __name__ == '__main__':
    load_GFS_analysis(select_date='2024-08-16', place='Europe')