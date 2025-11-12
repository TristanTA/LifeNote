import streamlit as st

from app.ui.side_bar import render_side_bar
from app.ui.main_screen import render_home
from data.init_managers import init_managers

def main():
    page = render_side_bar()
    if page == "Home":
        managers = init_managers()
        session = render_home()
        managers["raw_data_manager"].store_session(session)
    if page == "Raw Logs":
        st.title("Raw Logs")
        st.write("This is where raw logs will be displayed.")

if __name__ == "__main__":
    main()