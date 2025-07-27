
from pathlib import Path
from datetime import datetime
from utils.db_manager import Note
from utils.json_manager import load_folder_index, save_folder_index, add_note_to_index
from utils.classifier_llm import classify_with_llm
from sentence_transformers import SentenceTransformer
import faiss
import json

EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def save_new_note(note_text: str, audio_path: str | None = None):
    result = classify_with_llm(note_text)
    folder_path = result.folder_path
    folder_dir = Path("data") / Path(folder_path)
    folder_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    note_id = f"note_{ts}"
    filename = f"{note_id}.md"
    file_path = folder_dir / filename
    file_path.write_text(note_text, encoding="utf-8")

    audio_dest = None
    if audio_path:
        audio_src = Path(audio_path)
        audio_dest = folder_dir / audio_src.name
        audio_src.rename(audio_dest)  # Moves the file

    index = load_folder_index()
    add_note_to_index(index, folder_path, note_id, filename, result.tags)
    save_folder_index(index)

    n = Note.create(
        content=note_text,
        audio_path=str(audio_dest) if audio_dest else None,
        folder_path=folder_path,
        tags=", ".join(result.tags),
        created_at=datetime.now(),
    )

    return {
        "note_id": note_id,
        "folder_path": folder_path,
        "tags": result.tags
    }
