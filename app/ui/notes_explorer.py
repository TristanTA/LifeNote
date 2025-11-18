import streamlit as st
import os

ROOT = "notes/"

def render_notes_explorer():
    os.makedirs(ROOT, exist_ok=True)

    if "nav_stack" not in st.session_state:
        st.session_state.nav_stack = []

    current_path = os.path.join(ROOT, *st.session_state.nav_stack)

    st.title("Notes Explorer")

    dirs, files = list_directory(current_path)

    if st.session_state.nav_stack:
        if st.button("⬅ Back"):
            st.session_state.nav_stack.pop()

    st.write("Folders")
    for d in dirs:
        if st.button(f"{d}", key=f"dir-{d}"):
            st.session_state.nav_stack.append(d)

    st.write("Files")
    selected_file = None
    for f in files:
        if st.button(f"{f}", key=f"file-{f}"):
            selected_file = os.path.join(current_path, f)

    if selected_file:
        st.write("---")
        st.subheader(f"Viewing: {os.path.basename(selected_file)}")

        if selected_file.endswith(".txt") or selected_file.endswith(".md"):
            with open(selected_file, "r", encoding="utf-8") as f:
                st.code(f.read(), language="markdown")
        elif selected_file.endswith(".pdf"):
            st.write("PDF Preview:")
            st.pdf(selected_file)
        else:
            st.warning("No preview available for this file type.")

def list_directory(path: str):
    items = os.listdir(path)
    dirs = []
    files = []

    for item in items:
        full = os.path.join(path, item)
        if os.path.isdir(full):
            dirs.append(item)
        else:
            files.append(item)

    return sorted(dirs), sorted(files)