import streamlit as st
from src import (
    get_user_settings,
    set_user_settings,
    update_user_settings,
    delete_user_settings,
    add_more_user_settings,
)

st.header("Profil")

# Assuming `username` is obtained after user login
username = st.session_state.logged_user  # replace with the actual logged-in username

# Load the user's current settings
user_settings = get_user_settings(username)


col1, col2, col3 = st.columns([4, 2, 20])
new_val = col1.chat_input("Say something")
fav_val = col2.checkbox(label=":star:")

if new_val and fav_val:
    add_more_user_settings(username, "settings_1", new_val)
    st.rerun()


# ------------ MANAGE SETTINGS [DELETE, MODIFY] ----------------------------------

# Allow the user to select a color theme
color_theme = st.selectbox("Color theme :", ["Light", "Dark", "System"])
settings_1 = st.multiselect(
    "Settings 1  :",
    options=user_settings.get("settings_1"),
    default=user_settings.get("settings_1"),
)


# Save settings button
if st.button("Save Settings", use_container_width=True):
    new_settings = {
        "color_theme": color_theme,
        "settings_1": settings_1,
    }
    set_user_settings(username, new_settings)
    st.success("Settings saved successfully!")


# Option to delete settings
if st.button("Delete Settings", use_container_width=True):
    delete_user_settings(username)
    st.success("Settings deleted successfully!")

user_updated = get_user_settings(username)
st.write(user_updated)
