import streamlit as st

from app.ui.side_bar import render_side_bar
from app.ui.main_screen import render_home
from data.init_managers import init_managers
from app.ui.settings.settings_page import render_settings
from app.ui.settings.theme import load_preferences, apply_theme

def main():
    if "theme" not in st.session_state:
        st.session_state.theme = "Default"
        print(f"main.py: Set session_state.theme = {st.session_state.theme}")
    else:
        print(f"main.py: Theme already in session_state = {st.session_state.theme}")
    
    apply_theme(st.session_state.theme)

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    page = render_side_bar()
    if page:
        st.session_state["page"] = page

    if st.session_state["page"] == "Home":
        managers = init_managers()
        session = render_home()
        managers["raw_data_manager"].store_session(session)
    elif st.session_state["page"] == "Raw Logs":
        st.title("Raw Logs")
        st.write("This is where raw logs will be displayed.")
    elif st.session_state["page"] == "Settings":
        render_settings()
        print("Main render settings theme", st.session_state.theme)


if __name__ == "__main__":
    main()