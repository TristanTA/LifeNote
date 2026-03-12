from langchain.tools import tool
from instances.db_instance import db


@tool
def create_input_tool(
    input_type: str,
    content_text: str | None = None,
    file_path: str | None = None,
    source: str | None = None,
) -> int:
    """
    Purpose: Create a new raw input item in the inbox table.
    Args: input_type (text/audio/image/video/file), content_text (optional raw text), file_path (optional file path), source (optional source label).
    Returns: The integer ID of the created input.
    """
    print(f"[TOOLS] create_input_tool(input_type={input_type}, content_text_length={len(content_text) if content_text else 0}, file_path={file_path}, source={source})")
    return db.create_input(
        input_type=input_type,
        content_text=content_text,
        file_path=file_path,
        source=source,
    )


@tool
def get_input_tool(input_id: int) -> dict | None:
    """
    Purpose: Get one raw input item by ID.
    Args: input_id (integer input ID).
    Returns: The input row as a dict, or None if not found.
    """
    print(f"[TOOLS] get_input_tool(input_id={input_id})")
    row = db.get_input(input_id)
    return dict(row) if row else None


@tool
def list_inputs_tool() -> list[dict]:
    """
    Purpose: List all raw inputs.
    Args: None.
    Returns: A list of input rows as dicts.
    """
    print("[TOOLS] list_inputs_tool()")
    rows = db.list_inputs()
    return [dict(r) for r in rows]


@tool
def list_pending_inputs_tool() -> list[dict]:
    """
    Purpose: List all pending raw inputs that still need processing.
    Args: None.
    Returns: A list of pending input rows as dicts.
    """
    print("[TOOLS] list_pending_inputs_tool()")
    rows = db.list_pending_inputs()
    return [dict(r) for r in rows]


@tool
def set_input_status_tool(input_id: int, status: str, error: str | None = None) -> str:
    """
    Purpose: Update the processing status of a raw input item.
    Args: input_id (integer input ID), status (pending/processing/done/failed), error (optional error message).
    Returns: A status string.
    """
    print(f"[TOOLS] set_input_status_tool(input_id={input_id}, status={status}, error={error})")
    db.set_input_status(input_id=input_id, status=status, error=error)
    return f"Input {input_id} marked as {status}."


@tool
def delete_input_tool(input_id: int) -> str:
    """
    Purpose: Delete a raw input item by ID.
    Args: input_id (integer input ID).
    Returns: A status string.
    """
    print(f"[TOOLS] delete_input_tool(input_id={input_id})")
    db.delete_input(input_id)
    return f"Deleted input {input_id}."


@tool
def create_note_tool(
    input_id: int | None = None,
    title: str | None = None,
    transcript: str | None = None,
    summary: str = "",
    full_text: str | None = None,
    folder: str | None = None,
    tags: str | None = None,
) -> int:
    """
    Purpose: Create a processed note from an input item.
    Args: input_id (optional source input ID), title (optional title), transcript (optional transcript), summary (required summary), full_text (optional extracted text), folder (optional folder), tags (optional tags).
    Returns: The integer ID of the created note.
    """
    print(f"[TOOLS] create_note_tool(input_id={input_id}, title={title}, transcript_length={len(transcript) if transcript else 0}, summary_length={len(summary)}, full_text_length={len(full_text) if full_text else 0}, folder={folder}, tags={tags})")
    return db.create_note(
        input_id=input_id,
        title=title,
        transcript=transcript,
        summary=summary,
        full_text=full_text,
        folder=folder,
        tags=tags,
    )


@tool
def get_note_tool(note_id: int) -> dict | None:
    """
    Purpose: Get one processed note by ID.
    Args: note_id (integer note ID).
    Returns: The note row as a dict, or None if not found.
    """
    print(f"[TOOLS] get_note_tool(note_id={note_id})")
    row = db.get_note(note_id)
    return dict(row) if row else None


@tool
def get_note_by_input_id_tool(input_id: int) -> dict | None:
    """
    Purpose: Get a processed note linked to a specific input item.
    Args: input_id (integer input ID).
    Returns: The note row as a dict, or None if not found.
    """
    print(f"[TOOLS] get_note_by_input_id_tool(input_id={input_id})")
    row = db.get_note_by_input_id(input_id)
    return dict(row) if row else None


@tool
def list_notes_tool() -> list[dict]:
    """
    Purpose: List all processed notes in reverse chronological order.
    Args: None.
    Returns: A list of note rows as dicts.
    """
    print("[TOOLS] list_notes_tool()")
    rows = db.list_notes()
    return [dict(r) for r in rows]


@tool
def update_note_tool(
    note_id: int,
    title: str | None = None,
    transcript: str | None = None,
    summary: str | None = None,
    full_text: str | None = None,
    folder: str | None = None,
    tags: str | None = None,
) -> str:
    """
    Purpose: Update an existing processed note.
    Args: note_id (integer note ID), title (optional), transcript (optional), summary (optional), full_text (optional), folder (optional), tags (optional).
    Returns: A status string.
    """
    print(f"[TOOLS] update_note_tool(note_id={note_id}, title={title}, transcript_length={len(transcript) if transcript else 0}, summary_length={len(summary) if summary else 0}, full_text_length={len(full_text) if full_text else 0}, folder={folder}, tags={tags})")
    db.update_note(
        note_id=note_id,
        title=title,
        transcript=transcript,
        summary=summary,
        full_text=full_text,
        folder=folder,
        tags=tags,
    )
    return f"Updated note {note_id}."


@tool
def delete_note_tool(note_id: int) -> str:
    """
    Purpose: Delete a processed note by ID.
    Args: note_id (integer note ID).
    Returns: A status string.
    """
    print(f"[TOOLS] delete_note_tool(note_id={note_id})")
    db.delete_note(note_id)
    return f"Deleted note {note_id}."


@tool
def set_memory_tool(key: str, value: str) -> str:
    """
    Purpose: Save or update a memory value by key.
    Args: key (memory key), value (memory value).
    Returns: A status string.
    """
    print(f"[TOOLS] set_memory_tool(key={key}, value_length={len(value)})")
    db.set_memory(key, value)
    return f"Memory set for key '{key}'."


@tool
def get_memory_tool(key: str) -> str | None:
    """
    Purpose: Get a stored memory value by key.
    Args: key (memory key).
    Returns: The stored value, or None if not found.
    """
    print(f"[TOOLS] get_memory_tool(key={key})")
    return db.get_memory(key)


@tool
def add_embedding_tool(note_id: int, vector: bytes) -> str:
    """
    Purpose: Save or update an embedding vector for a note.
    Args: note_id (note ID), vector (serialized embedding bytes).
    Returns: A status string.
    """
    print(f"[TOOLS] add_embedding_tool(note_id={note_id}, vector_bytes={len(vector)})")
    db.add_embedding(note_id, vector)
    return f"Embedding saved for note {note_id}."


@tool
def get_embedding_tool(note_id: int) -> bytes | None:
    """
    Purpose: Get the stored embedding vector for a note.
    Args: note_id (note ID).
    Returns: The embedding bytes, or None if not found.
    """
    print(f"[TOOLS] get_embedding_tool(note_id={note_id})")
    row = db.get_embedding(note_id)
    if not row:
        return None
    return row["vector"]


@tool
def set_user_tool(name: str | None = None, preferences: str | None = None) -> str:
    """
    Purpose: Create or update the single user profile.
    Args: name (optional user name), preferences (optional serialized preferences).
    Returns: A status string.
    """
    print(f"[TOOLS] set_user_tool(name={name}, preferences_length={len(preferences) if preferences else 0})")
    db.set_user(name=name, preferences=preferences)
    return "User profile updated."


@tool
def get_user_tool() -> dict | None:
    """
    Purpose: Get the single user profile.
    Args: None.
    Returns: The user row as a dict, or None if not found.
    """
    print("[TOOLS] get_user_tool()")
    row = db.get_user()
    return dict(row) if row else None


DB_TOOLS = [
    create_input_tool,
    get_input_tool,
    list_inputs_tool,
    list_pending_inputs_tool,
    set_input_status_tool,
    delete_input_tool,
    create_note_tool,
    get_note_tool,
    get_note_by_input_id_tool,
    list_notes_tool,
    update_note_tool,
    delete_note_tool,
    set_memory_tool,
    get_memory_tool,
    add_embedding_tool,
    get_embedding_tool,
    set_user_tool,
    get_user_tool,
]