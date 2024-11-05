import streamlit as st
from src import verify_password, load_user_data

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logged_user" not in st.session_state:
    st.session_state.logged_user = ''

if "logged_fullname" not in st.session_state:
    st.session_state.logged_fullname = ''

if "logged_profil" not in st.session_state:
    st.session_state.logged_profil = ''

def login():
    st.sidebar.write('Welcome to MarketData')
    user = st.sidebar.text_input('Username', type='default')
    pwd = st.sidebar.text_input('Password', type='password')
    connect = st.sidebar.button("Log in", use_container_width=True, type='primary')
    if connect:
        if verify_password(user, pwd):
            user_data = load_user_data()
            st.session_state.logged_in = True
            st.session_state.logged_user = user
            st.session_state.logged_fullname = user_data[user]['fullname']
            st.session_state.logged_profil = user_data[user]['profil']
            st.rerun()
        else:
            st.sidebar.error("Login failed. Please check your username and password.")

def logout():
    st.session_state.logged_in = False
    st.rerun()

active_user = st.session_state.logged_user
active_profil = st.session_state.logged_profil

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title=f"{active_user}", icon=f":material/logout:")

page0 = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
page1 = st.Page("pages/weather.py", title="Weather", icon=":material/partly_cloudy_day:")
page2 = st.Page("pages/cftc.py", title="CFTC", icon=":material/monitoring:")

page4 = st.Page("pages/cash.py", title="Grains", icon=":material/compost:")
page5 = st.Page("pages/fret.py", title="Freight", icon=":material/directions_boat:")

page10 = st.Page("pages/profile.py", title="Profile", icon=":material/account_circle:")
page11 = st.Page("pages/admin.py", title="Admin", icon=":material/settings:")

if st.session_state.logged_in:
    if active_profil in ['admin']:
        pg = st.navigation(
                {
                    "Account": [logout_page],
                    "Financial market": [page0, page1, page2],
                    "Cash market": [page4, page5],
                    "Administration": [page10, page11],
                }
            )
    elif active_profil in ['trader', 'analyst']:
        pg = st.navigation(
                {
                    "Account": [logout_page],
                    "Financial market": [page0, page1, page2],
                    "Cash market": [page4, page5],
                    "Administration": [page10],
                }
            )
else:
    pg = st.navigation([login_page])

pg.run()