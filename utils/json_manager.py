import json
from pathlib import Path

INDEX_PATH = Path("data/folder_index.json")

def ensure_folder_index(DEBUG = False):
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

def load_folder_index():
    ensure_folder_index()
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))

def save_folder_index(index_data):
    INDEX_PATH.write_text(json.dumps(index_data, indent=2), encoding="utf-8")