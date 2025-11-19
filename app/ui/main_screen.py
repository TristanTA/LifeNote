import streamlit as st
from pathlib import Path
import json

from data.schemas.session_schema import Session
from app.ui.text_entry import render_text_entry
from agents.categorizer import categorize_text
from agents.organizer import get_file_path
from app.ui.editor import render_editor_content


def render_home():
    if "editor_data" not in st.session_state:
        st.session_state.editor_data = {"time": 0, "blocks": [], "version": "2.30.7"}
    if "current_session" not in st.session_state:
        st.session_state.current_session = Session(text=[])

    session_obj = st.session_state.current_session
    text_content = render_text_entry()

    if session_obj.text:
        st.markdown("---")
        st.subheader("Live Preview")
        last = session_obj.text[-1]
        if "blocks" in last.content:
            render_editor_content(last.content["blocks"])

    st.button("Save Session", on_click=save_session,
              args=(session_obj, text_content))

def save_session(session: Session, text_content):
    if text_content:
        text_object = categorize_text(text_content)
        session.add_text(text_object)

    file_path = Path(get_file_path(session))
    file_path.parent.mkdir(parents=True, exist_ok=True)

    content = session.to_dict()

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    st.session_state.current_session = Session(text=[])
    st.session_state.editor_data = {"time": 0, "blocks": [], "version": "2.30.7"}
    st.rerun()