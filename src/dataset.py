import os
import pandas as pd
from datetime import date, datetime

'''

Model GFS
Anomalies temperatures 1-7 jours :  https://www.worldagweather.com/fcstwx/tmp_gefs_day7_in_metric_2440.png
Precipitation 1-7 jours :           https://www.worldagweather.com/fcstwx/pcp_gfs_day7_in_metric_2440.png
Past anomalies 7 day total :        https://www.worldagweather.com/pastwx/pastpcp_in_7day_metric_4433.png

'''

dict_refid = {
    'temp_gefs_day7':[2440, '2024-08-18'],
    'pcp_gfs_day7':[2441, '2024-08-18'],
    'pastpcp_in_7day':[4433, '2024-08-16'],
    }

dict_place = {
    'North America': 'na',
    'Europe':'eu',
    'USA':'us',
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

def load_temp_anomaly(select_date:str, place:str) -> object:
    id_date = calculate_id_date(select_date, type='temp_gefs_day7')
    id_place = dict_place[place]
    url = f'https://www.worldagweather.com/fcstwx/tmp_gefs_day7_{id_place}_metric_{id_date}.png'

    return url


if __name__ == '__main__':
    load_temp_anomaly(select_date='2024-08-16', place='Europe')