import streamlit as st
from inputs.audio.ui import display_audio_ui

def main():
    st.title("LifeNotes")

    audio_text = display_audio_ui()

    st.success(audio_text)

if __name__ == "__main__":
    main() 