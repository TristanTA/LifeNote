import json
from pathlib import Path
from datetime import datetime

INDEX_PATH = Path("data/folder_index.json")

def ensure_folder_index(DEBUG=False):
    """Ensure that folder_index.json exists with a default structure."""
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not INDEX_PATH.exists():
        if DEBUG: 
            print("No folder_index.json found.")
        empty_index = {
            "root": {
                "summary": "Root folder for all notes.",
                "children": {}
            }
        }
        save_folder_index(empty_index)
        if DEBUG:
            print("Created empty folder_index.json")

def load_folder_index(DEBUG=False):
    ensure_folder_index(DEBUG)
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))

def save_folder_index(index_data, DEBUG=False):
    INDEX_PATH.write_text(json.dumps(index_data, indent=2), encoding="utf-8")
    if DEBUG:
        print("Saving updated folder_index.json.")
        
def add_note_to_index(index, folder_path, note_id, filename, tags, DEBUG=False):
    """
    Add a new note to the folder_index at the correct path.
    Creates folders as needed.
    """
    path_parts = folder_path.strip("/").split("/")
    current = index["root"]

    for part in path_parts:
        if "children" not in current:
            current["children"] = {}
        if part not in current["children"]:
            current["children"][part] = {
                "summary": "",
                "children": {}
            }
        current = current["children"][part]

    if "notes" not in current:
        current["notes"] = []

    # Append the new note
    current["notes"].append({
        "id": note_id,
        "filename": filename,
        "created_at": datetime.now().isoformat(),
        "tags": tags
    })
    if DEBUG:
        print(f"Added {filename} to folder_index.json. Tags: {tags}.")