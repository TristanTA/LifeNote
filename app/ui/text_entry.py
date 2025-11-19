import streamlit as st
from streamlit_editorjs_component import streamlit_editorjs
from data.schemas.text_schema import Text

def render_text_entry():
    if "editor_data" not in st.session_state:
        st.session_state.editor_data = {"time": 0, "blocks": [], "version": "2.30.7"}
    editor_output = streamlit_editorjs(
        key="editor_input",
        data=st.session_state.editor_data
    )
    if editor_output:
        st.session_state.editor_data = editor_output
    return Text(content=st.session_state.editor_data)