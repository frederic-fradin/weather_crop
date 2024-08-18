import streamlit as st
from src import load_places, load_GFS_analysis, image_rectangle, crop_image

tab1, tab2, tab3 = st.tabs(['GFS Analysis', '...', '...'])

def_url = 'https://www.worldagweather.com/fcstwx/pcp_gfs_day7_in_metric_2440.png'

with tab1:
    st.write('')
    col1, col2, col3, col4, col5 = st.columns([2,2,2,2,2])
    sel_place = col1.selectbox('Place', key='tp1', options=load_places(), index=0, label_visibility='collapsed')
    sel_date = col2.date_input("Date", key='tp2', format="YYYY-MM-DD", label_visibility='collapsed')
    validate = col3.button('Show', key='tp3', use_container_width=True)

    if validate:
        st.write('')
        col1b, col2b, col3b = st.columns([3,3,3])
        url1, url2, url3 = load_GFS_analysis(select_date=str(sel_date), place=sel_place)
        col1b.image(url1, use_column_width=True)
        col2b.image(url2, use_column_width=True)
        col3b.image(url3, use_column_width=True)


with tab2:
    st.write('')
    col1, col2, col3, col4, col5 = st.columns([2,2,2,2,2])
    top = col1.number_input('Top corner', key='top', step=1, min_value=1)
    left = col2.number_input('Left corner', key='left', step=1, min_value=1)
    bottom = col3.number_input('Bottom corner', key='bottom', step=1, min_value=1)
    right = col4.number_input('Right corner', key='Right', step=1, min_value=1)
    shape = col5.selectbox('Shape', options=['rectangle', 'ellipse'], index=0)
    validate = st.button('Show and crop', key='rec5', use_container_width=True)

    if validate:
        st.write('')
        col1, col2 = st.columns([5,5])
        img1 = image_rectangle(url=def_url,
                        left=left, top=top, right=right, bottom=bottom,
                        forme=shape)
        col1.image(img1)

        img2, img3, color_ref = crop_image(url=def_url,
                        left=left, top=top, right=right, bottom=bottom,
                        )
        col2.image(img2)
        col2.image(img3)
        col2.write(color_ref)
