import os
import pandas as pd
import streamlit as st
from datetime import date, datetime, timedelta

directory = os.path.dirname(os.path.abspath(__file__))

'''

Model GFS
Anomalies temperatures 1-7 jours :  https://www.worldagweather.com/fcstwx/tmp_gefs_day7_in_metric_2440.png
Precipitation 1-7 jours :           https://www.worldagweather.com/fcstwx/pcp_gfs_day7_in_metric_2440.png
Past anomalies 7 day total :        https://www.worldagweather.com/pastwx/pastpcp_in_7day_metric_4433.png
Precipitation anomalies 14j :       https://www.worldagweather.com/pastwx/pastpcp_anom_na_14day_4509.png


Precipitation anomalies wheat :     https://www.worldagweather.com/crops/fcstwx/fcsttmpmap_wheat_europe_metric_4481.png
                                    https://www.worldagweather.com/crops/pastwx/pasttmpmap_wheat_europe_60day_metric_4479.png
                                    https://www.worldagweather.com/crops/fcstwx/fcstpcpmap_wheat_europe_4482.png
                                    https://www.worldagweather.com/crops/pastwx/pastpcpmap_wheat_europe_60day_4487.png



Map of production par product
https://ipad.fas.usda.gov/cropexplorer/cropview/commodityView.aspx?cropid=0440000


'''

dict_refid = {
    'tmp_gefs_day7':[2516, '2024-11-2'],
    'pcp_gfs_day7':[2516, '2024-11-2'],
    'pastpcp_in_7day':[4509, '2024-11-2'],
    'pastpcp_anom':[4509, '2024-11-2'],
    'fcsttmpmap_wheat':[4481, '2024-11-2'],
    'pasttmpmap_wheat':[4479, '2024-11-2'],
    'fcstpcpmap_wheat':[4482, '2024-11-2'],
    'pastpcpmap_wheat':[4487, '2024-11-2']
    }

dict_place = {
    'Canada': ['na', 'wheat_canada'],
    'United-States': ['us', 'wheat_usa'],
    'Europe':['eu', 'wheat_europe'],
    'South America (North)':['br', 'corn_brazil'],
    'South America (South)':['ar', 'corn_argentina'],
    'West Asia':['wa', 'wheat_ukraine'],
    'East Asia':['cn', 'corn_china'],
    'Australia':['au', 'wheat_australia'],
    'India':['in', 'wheat_india'],
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

@st.cache_data(ttl=timedelta(hours=1))
def load_GFS_analysis(select_date:str, place:str) -> object:
    id_place = dict_place[place][0]

    id1 = calculate_id_date(select_date, type='tmp_gefs_day7')
    url1 = f'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_{id_place}_metric_{id1}.png'

    id2 = calculate_id_date(select_date, type='pcp_gfs_day7')
    url2 = f'https://www.worldagweather.com/fcstwx/pcp_gfs_day7_{id_place}_metric_{id2}.png'

    id3 = calculate_id_date(select_date, type='pastpcp_in_7day')
    url3 = f'https://www.worldagweather.com/pastwx/pastpcp_{id_place}_7day_metric_{id3}.png'

    id4 = calculate_id_date(select_date, type='pastpcp_anom')
    url4 = f'https://www.worldagweather.com/pastwx/pastpcp_anom_{id_place}_14day_{id4}.png'

    return url1, url2, url3, url4

@st.cache_data(ttl=timedelta(hours=1))
def load_crop_analysis(select_date:str, place:str) -> object:
    id_place = dict_place[place][1]

    id1 = calculate_id_date(select_date, type='fcsttmpmap_wheat')
    url1 = f'https://www.worldagweather.com/crops/fcstwx/fcsttmpmap_{id_place}_metric_{id1}.png'

    id2 = calculate_id_date(select_date, type='pasttmpmap_wheat')
    url2 = f'https://www.worldagweather.com/crops/pastwx/pasttmpmap_{id_place}_60day_metric_{id2}.png'

    id3 = calculate_id_date(select_date, type='fcstpcpmap_wheat')
    url3 = f'https://www.worldagweather.com/crops/fcstwx/fcstpcpmap_{id_place}_{id2}.png'

    id4 = calculate_id_date(select_date, type='pastpcpmap_wheat')
    url4 = f'https://www.worldagweather.com/crops/pastwx/pastpcpmap_{id_place}_60day_{id2}.png'

    return url1, url2, url3, url4

@st.cache_data(ttl=timedelta(hours=1))
def load_GFS_anomaly(select_date:str, place:str) -> object:
    id_place = dict_place[place][0]

    id1 = calculate_id_date(select_date, type='tmp_gefs_day7')
    url1 = f'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_{id_place}_metric_{id1}.png'

    return url1

@st.cache_data(ttl=timedelta(hours=1))
def load_crop_calendar():
    file_path = os.path.join(directory, '../data/processed/crop_calendar.xlsx')
    data = pd.read_excel(file_path, sheet_name='Feuil1')

    region = data['REGION'].unique()
    product = data['PRODUCTION'].unique()

    return data, region, product

if __name__ == '__main__':
    load_GFS_analysis(select_date='2024-08-16', place='Europe')