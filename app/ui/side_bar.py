import streamlit as st

def render_side_bar():
    st.sidebar.title("LifeNotes")
    home_btn = st.sidebar.button("Home", type="tertiary", use_container_width=True)
    kahnban_btn = st.sidebar.button("Kahn ban", type="tertiary", use_container_width=True)
    notes_explorer_btn = st.sidebar.button("Notes Explorer", type="tertiary", use_container_width=True)
    settings_btn = st.sidebar.button("Settings", type="tertiary", use_container_width=True)
    if home_btn:
        return "Home"
    elif kahnban_btn:
        return "Kahnban"
    elif notes_explorer_btn:
        return "Notes Explorer"
    elif settings_btn:
        return "Settings"
    else:
        return None