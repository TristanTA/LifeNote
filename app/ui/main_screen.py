import streamlit as st

from app.ui.text_entry import render_text_entry

def render_main_screen():
    st.title("LifeNotes")
    render_text_entry()