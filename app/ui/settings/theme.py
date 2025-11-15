import streamlit as st
import json
import os

themes = {
    "Default": {
    "primaryColor": "#2345FF",
    "backgroundColor": "#F8F9FB",
    "secondaryBackgroundColor": "#E6E8EE",
    "textColor": "#1A1C20",
    "font": "times new roman",
    },
    "Amber Fog": {
    "primaryColor": "#D4A056",
    "backgroundColor": "#F8F7F5",
    "secondaryBackgroundColor": "#E9E7E3",
    "textColor": "#2C2824",
    "font": "times new roman",
    },
    "Coastal Fog": {
    "primaryColor": "#5E8BAE",
    "backgroundColor": "#F7F9FB",
    "secondaryBackgroundColor": "#E4E8EC",
    "textColor": "#1D2125",
    "font": "times new roman",
    },
    "Fieldstone": {
        "primaryColor": "#A9A191",
        "backgroundColor": "#F6F6F5",
        "secondaryBackgroundColor": "#E7E6E3",
        "textColor": "#232221",
        "font": "times new roman",
    },
    "Graphite Calm": {
    "primaryColor": "#8AA0B4",
    "backgroundColor": "#15181C",
    "secondaryBackgroundColor": "#1E2228",
    "textColor": "#E7E9ED",
    "font": "times new roman",
    },
    "Sage Mist": {
    "primaryColor": "#7BA693",
    "backgroundColor": "#F3F5F4",
    "secondaryBackgroundColor": "#E3E8E5",
    "textColor": "#242A28",
    "font": "times new roman",
    },
    "Warm Neutral": {
    "primaryColor": "#C17F59",
    "backgroundColor": "#FAF7F4",
    "secondaryBackgroundColor": "#ECE6E1",
    "textColor": "#2B2521",
    "font": "times new roman",
    },
}


PREFERENCES_FILE = "data/user/preferences.json"

def load_preferences():
    if not os.path.exists(PREFERENCES_FILE):
        default = {"theme": "Fieldstone"}
        os.makedirs(os.path.dirname(PREFERENCES_FILE), exist_ok=True)
        with open(PREFERENCES_FILE, "w") as f:
            json.dump(default, f, indent=4)
        return default
    with open(PREFERENCES_FILE, "r") as f:
        return json.load(f)

def save_preferences(prefs):
    with open(PREFERENCES_FILE, "w") as f:
        json.dump(prefs, f, indent=4)

def apply_theme(theme):
    print("theme75 theme", theme)
    if isinstance(theme, str):
        theme = themes[theme]
    if isinstance(theme, dict):
        theme = theme

    primary = theme["primaryColor"]
    bg = theme["backgroundColor"]
    sbg = theme["secondaryBackgroundColor"]
    text = theme["textColor"]
    font = theme["font"]

    st.markdown(f"""
        <style>
        /* General Layout */
        html, body, [class*="css"]  {{
            color: {text};
            background-color: {bg};
            font-family: '{font}', sans-serif;
        }}

        section[data-testid="stSidebar"] {{
            background-color: {sbg};
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {primary};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            transition: all 0.2s ease;
        }}
        .stButton > button:hover {{
            background-color: {primary}CC; /* slight transparency */
            transform: translateY(-1px);
        }}

        /* Text Input and Text Area */
        .stTextInput > div > div > input,
        textarea {{
            background-color: {sbg};
            color: {text};
            border-radius: 6px;
            border: 1px solid {primary}33;
        }}
        .stTextInput > div > div > input:focus,
        textarea:focus {{
            outline: none !important;
            border: 1px solid {primary};
            box-shadow: 0 0 0 1px {primary};
        }}

        /* Selectbox & Multiselect */
        div[data-baseweb="select"] > div {{
            background-color: {sbg};
            color: {text};
            border-radius: 6px;
            border: 1px solid {primary}33;
        }}
        div[data-baseweb="select"]:focus-within {{
            border-color: {primary};
            box-shadow: 0 0 0 1px {primary};
        }}

        /* Slider */
        [data-testid="stSlider"] > div {{
            color: {primary};
        }}
        [data-testid="stSlider"] .stSliderTrack {{
            background: linear-gradient(to right, {primary}, {primary}CC);
        }}

        /* Checkbox & Radio */
        label[data-baseweb="checkbox"] > div:first-child,
        label[data-baseweb="radio"] > div:first-child {{
            border-color: {primary};
        }}
        label[data-baseweb="checkbox"] input:checked + div:first-child,
        label[data-baseweb="radio"] input:checked + div:first-child {{
            background-color: {primary};
            border-color: {primary};
        }}

        /* Expander and Containers */
        .streamlit-expanderHeader {{
            background-color: {sbg};
            color: {text};
            border-radius: 6px;
        }}
        .streamlit-expanderHeader:hover {{
            background-color: {primary}1A;
        }}

        /* Tables */
        table {{
            border-collapse: collapse;
            width: 100%;
            color: {text};
        }}
        th, td {{
            border: 1px solid {sbg};
            padding: 0.5rem;
        }}
        th {{
            background-color: {sbg};
            color: {text};
        }}
        tr:nth-child(even) {{
            background-color: {bg};
        }}
        tr:hover {{
            background-color: {primary}1A;
        }}

        /* Progress Bars and Spinners */
        div[data-testid="stProgressBar"] div[role="progressbar"] {{
            background-color: {primary};
        }}

        /* Markdown links */
        a {{
            color: {primary};
        }}
        a:hover {{
            color: {primary}CC;
            text-decoration: underline;
        }}
        </style>
    """, unsafe_allow_html=True)
    print("Apply function Theme", st.session_state.theme)
    return st.session_state["theme"]

def render_theme_settings():
    current_theme = st.session_state.theme
    print(f"render_theme_settings: current_theme from session_state = {current_theme}")

    selected = st.selectbox(
        "Choose a theme",
        list(themes.keys())
    )
    print(f"render_theme_settings: selected from selectbox = {selected}")

    if selected != current_theme:
        print(f"render_theme_settings: Theme changed from {current_theme} to {selected}")
        st.session_state.theme = selected
        print(f"render_theme_settings: Updated session_state.theme = {st.session_state.theme}")
        
        # Save to file
        prefs_to_save = {"theme": selected}
        print(f"render_theme_settings: Saving to file: {prefs_to_save}")
        save_preferences(prefs_to_save)
        
        # Verify it was saved
        loaded = load_preferences()
        print(f"render_theme_settings: Verified file contents: {loaded}")
        
        st.success(f"Theme changed to {selected}")
        st.rerun()
    else:
        print(f"render_theme_settings: No change detected, selected={selected}, current={current_theme}")

    st.write(f"Active theme: {st.session_state['theme']}")