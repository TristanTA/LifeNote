import streamlit as st
import pickle

from data.schemas.session_schema import Session
from app.ui.text_entry import render_text_entry
from agents.categorizer import categorize_text
from agents.organizer import get_file_path

def render_home():
    st.title("LifeNotes")
    st.session_state.current_session = Session(text=[])
    text_content = render_text_entry()
    text_object = categorize_text(text_content)
    st.session_state.current_session.add_text(text_object)
    session_obj = st.session_state.current_session

    st.button("Save Session", on_click=save_session(session_obj))

    return st.session_state.current_session

def save_session(session: Session):
    file_path = get_file_path(session)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        pickle.dump(session, f)