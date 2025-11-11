import streamlit as st



def render_text_entry():
    def clear_input():
        st.session_state.chat_input = ""
    st.set_page_config(page_title="LifeNotes", layout="wide")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    st.markdown("""
        <style>
        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0e1117;
            padding: 1rem;
            border-top: 1px solid #333;
            display: flex;
            align-items: center;
            z-index: 999;
        }
        section.main > div {padding-bottom: 6rem;}
        </style>
    """, unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        st.write(f"**You:** {msg}")

    chat_col1, chat_col2 = st.columns([5, 1])
    with chat_col1:
        user_message = st.text_input("Type a message...", key="chat_input", placeholder="Send a message...", label_visibility="collapsed")

    with chat_col2:
        send_clicked = st.button("Send")

    if st.button("Send"):
        if user_message.strip():
            st.session_state.chat_history.append(user_message)
            clear_input()
            st.experimental_rerun()