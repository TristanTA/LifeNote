import streamlit as st

from app.ui.settings.theme import render_theme_settings

def render_settings():
    st.title("Settings")
    render_theme_settings()