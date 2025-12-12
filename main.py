import streamlit as st

from app.ui.side_bar import render_side_bar
from data.init_managers import init_managers
from app.ui.settings.theme import apply_theme

from app.ui.main_screen import render_home
from app.ui.kahnban import render_kahnban
from app.ui.notes_explorer import render_notes_explorer
from app.ui.settings.settings_page import render_settings

def main():
    apply_theme()
    managers = init_managers()

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    selected = render_side_bar()

    if selected is not None:
        st.session_state.page = selected
    if st.session_state["page"] == "Home":
        render_home()
    elif st.session_state["page"] == "Kahnban":
        render_kahnban()
    elif st.session_state["page"] == "Notes Explorer":
        render_notes_explorer()
    elif st.session_state["page"] == "Settings":
        render_settings()

if __name__ == "__main__":
    main()