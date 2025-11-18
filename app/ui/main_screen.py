import streamlit as st
from pathlib import Path

from data.schemas.session_schema import Session
from app.ui.text_entry import render_text_entry
from agents.categorizer import categorize_text
from agents.organizer import get_file_path


def render_home():
    if "current_session" not in st.session_state:
        st.session_state.current_session = Session(text=[])

    session_obj = st.session_state.current_session
    text_content = render_text_entry()

    st.button("Save Session", on_click=save_session, args=(session_obj, text_content))

    return session_obj


def save_session(session: Session, text_content):
    if text_content:
        text_object = categorize_text(text_content)
        session.add_text(text_object)
    file_path = Path(get_file_path(session))
    file_path.parent.mkdir(parents=True, exist_ok=True)

    content = session.get_all()

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    st.success("Session saved!")