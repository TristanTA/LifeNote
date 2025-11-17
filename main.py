import streamlit as st

from app.ui.side_bar import render_side_bar
from app.ui.main_screen import render_home
from data.init_managers import init_managers
from app.ui.settings.settings_page import render_settings
from app.ui.settings.theme import apply_theme
from app.ui.notes_explorer import render_notes_explorer

def main():
    apply_theme()
    managers = init_managers()

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    page = render_side_bar()
    if page:
        st.session_state["page"] = page

    if st.session_state["page"] == "Home":
        session = render_home()
        managers["raw_data_manager"].store_session(session)
    elif st.session_state["page"] == "Notes Explorer":
        render_notes_explorer()
    elif st.session_state["page"] == "Settings":
        render_settings()


if __name__ == "__main__":
    main()