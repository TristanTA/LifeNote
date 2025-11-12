import streamlit as st

from data.schemas.session_schema import Session

from app.ui.text_entry import render_text_entry

def render_home():
    st.title("LifeNotes")
    st.session_state.current_session = Session(text=[])
    text_content = render_text_entry()
    st.session_state.current_session.add_text(text_content)

    return st.session_state.current_session