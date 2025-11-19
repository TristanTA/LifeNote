import streamlit as st
import os
import json
from pathlib import Path
from streamlit_tree_select import tree_select
import ast

from app.ui.editor import render_editor_content

ROOT = "notes"


def render_notes_explorer():
    Path(ROOT).mkdir(parents=True, exist_ok=True)

    st.header("Notes Explorer")

    tree = build_notes_tree(ROOT)
    selection = tree_select(tree, check_model="all", no_cascade=True)

    if selection and selection["checked"]:
        filepath = selection["checked"][0]
        note = load_note_from_file(filepath)
        display_note_pretty(note)

def build_notes_tree(path):
    nodes = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)

        if os.path.isdir(full_path):
            nodes.append({
                "label": item,
                "value": full_path,
                "children": build_notes_tree(full_path)
            })
        else:
            nodes.append({
                "label": item,
                "value": full_path,
                "children": []
            })

    return nodes


def load_note_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        note = json.load(f)
    fixed_text = []
    for item in note.get("text", []):
        content = item.get("content")
        if isinstance(content, str):
            try:
                content = ast.literal_eval(content)
            except:
                content = {"blocks": []}
        item["content"] = content
        fixed_text.append(item)
    note["text"] = fixed_text
    note["path"] = path
    return note

def display_note_pretty(note):
    title = note["text"][0]["title"]
    st.subheader(title)
    st.caption(note.get("timestamp", ""))
    text_items = note.get("text", [])
    if len(text_items) == 0:
        st.info("This note has no content.")
        return
    content = text_items[0]["content"]
    blocks = content.get("blocks", [])
    render_editor_content(blocks)
    with st.expander("Metadata"):
        st.json({
            "note_id": note["id"],
            "note_timestamp": note["timestamp"],
            "text_id": note["text"][0]["id"],
            "text_timestamp": note["text"][0]["timestamp"],
            "tags": note["text"][0].get("tags", []),
            "title": note["text"][0].get("title", ""),
            "path": note.get("path", "N/A"),
        })

    if st.button("🗑 Delete Note", key="delete_note"):
        file_path = Path(note.get("path"))
        if file_path.exists():
            file_path.unlink()
            st.success("Note deleted!")
            current = file_path.parent
            root = Path(ROOT).resolve()
            while current != root:
                try:
                    if not any(current.iterdir()):
                        current.rmdir()
                    else:
                        break
                except OSError:
                    break
                current = current.parent
            st.rerun()