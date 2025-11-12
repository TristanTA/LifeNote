import streamlit as st



def render_side_bar():
    st.sidebar.title("LifeNotes")
    home_btn = st.sidebar.button("Home", type="tertiary", use_container_width=True)
    logs_btn = st.sidebar.button("Raw Logs", type="tertiary", use_container_width=True)
    if home_btn:
        return "Home"
    elif logs_btn:
        return "Raw Logs"
    else:
        return "Home"
