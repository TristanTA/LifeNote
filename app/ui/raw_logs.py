import sqlite3
import pandas as pd
import streamlit as st

from data.managers.store_raw import RawData

def render_raw_logs(raw_data_manager: RawData):
    st.title("Raw Logs Viewer")
    df = raw_data_manager.get_dataframe()
    st.dataframe(df)
