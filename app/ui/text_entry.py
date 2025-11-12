import streamlit as st
from streamlit_editorjs_component import streamlit_editorjs
from data.schemas.text_schema import Text

def render_text_entry():
    content = streamlit_editorjs()

    st.write("### Output:")
    st.json(content)
    package = Text(content=str(content))
    return package