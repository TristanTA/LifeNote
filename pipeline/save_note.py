# pipeline/save_note.py
from pathlib import Path
from datetime import datetime
from utils.db_manager import Note  # extend with folder_path, tags json, etc.
from utils.folder_index import load_index, save_index, add_note_to_index
from utils.classifier_llm import classify_with_llm
from sentence_transformers import SentenceTransformer
import faiss
import json

EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def save_new_note(note_text: str, audio_path: str | None = None):
    # classify
    result = classify_with_llm(note_text)
    folder_path = result.folder_path
    folder_dir = Path("data") / Path(folder_path)
    folder_dir.mkdir(parents=True, exist_ok=True)

    # write markdown file
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    note_id = f"note_{ts}"
    filename = f"{note_id}.md"
    file_path = folder_dir / filename
    file_path.write_text(note_text, encoding="utf-8")

    # update index
    index = load_index()
    add_note_to_index(index, folder_path, note_id, filename, result.tags)
    save_index(index)

    # store in DB (extend Note with folder_path, tags JSON/Text)
    n = Note.create(
        content=note_text,
        audio_path=audio_path,
        created_at=datetime.now(),
        # add these columns in your schema
        # folder_path=folder_path,
        # tags=json.dumps(result.tags)
    )

    # (optional now) embed & add to FAISS note index (do this when you build the global search index)

    return {
        "note_id": note_id,
        "folder_path": folder_path,
        "tags": result.tags
    }