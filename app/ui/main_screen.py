import streamlit as st

from data.schemas.session_schema import Session

from app.ui.text_entry import render_text_entry
from agents.categorizer import categorize_text

def render_home():
    st.title("LifeNotes")
    st.session_state.current_session = Session(text=[])
    text_content = render_text_entry()
    text_object = categorize_text(text_content)
    st.session_state.current_session.add_text(text_object)

    return st.session_state.current_session