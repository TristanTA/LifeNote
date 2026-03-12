import sqlite3
from pathlib import Path


class DB:
    def __init__(self, path="lifenotes.db"):
        self.path = Path(path)
        self._init_tables()

    # ---------- CONNECTION ----------

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # ---------- INIT ----------

    def _init_tables(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    name TEXT,
                    preferences TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS inputs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_type TEXT NOT NULL CHECK(input_type IN ('text', 'audio', 'image', 'video', 'file')),
                    content_text TEXT,
                    file_path TEXT,
                    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'done', 'failed')),
                    source TEXT,
                    error TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_at TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_id INTEGER UNIQUE,
                    title TEXT,
                    transcript TEXT,
                    summary TEXT NOT NULL,
                    full_text TEXT,
                    folder TEXT,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    FOREIGN KEY(input_id) REFERENCES inputs(id) ON DELETE SET NULL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER UNIQUE,
                    vector BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(note_id) REFERENCES notes(id) ON DELETE CASCADE
                )
            """)

            conn.commit()

    # ---------- GENERIC HELPERS ----------

    def execute(self, query, params=()):
        with self._connect() as conn:
            cur = conn.execute(query, params)
            conn.commit()
            return cur.lastrowid

    def fetchone(self, query, params=()):
        with self._connect() as conn:
            return conn.execute(query, params).fetchone()

    def fetchall(self, query, params=()):
        with self._connect() as conn:
            return conn.execute(query, params).fetchall()

    # ---------- INPUTS ----------

    def create_input(self, input_type, content_text=None, file_path=None, source=None):
        return self.execute("""
            INSERT INTO inputs (input_type, content_text, file_path, source)
            VALUES (?, ?, ?, ?)
        """, (input_type, content_text, file_path, source))

    def get_input(self, input_id):
        return self.fetchone("SELECT * FROM inputs WHERE id = ?", (input_id,))

    def list_inputs(self):
        return self.fetchall("SELECT * FROM inputs ORDER BY created_at DESC")

    def list_pending_inputs(self):
        return self.fetchall("""
            SELECT * FROM inputs
            WHERE status = 'pending'
            ORDER BY created_at ASC
        """)

    def set_input_status(self, input_id, status, error=None):
        if status in ("done", "failed"):
            self.execute("""
                UPDATE inputs
                SET status = ?, error = ?, processed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, error, input_id))
        else:
            self.execute("""
                UPDATE inputs
                SET status = ?, error = ?
                WHERE id = ?
            """, (status, error, input_id))

    def delete_input(self, input_id):
        self.execute("DELETE FROM inputs WHERE id = ?", (input_id,))

    # ---------- NOTES ----------

    def create_note(self, input_id=None, title=None, transcript=None, summary="", full_text=None, folder=None, tags=None):
        return self.execute("""
            INSERT INTO notes (input_id, title, transcript, summary, full_text, folder, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (input_id, title, transcript, summary, full_text, folder, tags))

    def get_note(self, note_id):
        return self.fetchone("SELECT * FROM notes WHERE id = ?", (note_id,))

    def get_note_by_input_id(self, input_id):
        return self.fetchone("SELECT * FROM notes WHERE input_id = ?", (input_id,))

    def list_notes(self):
        return self.fetchall("SELECT * FROM notes ORDER BY created_at DESC")

    def update_note(
        self,
        note_id,
        title=None,
        transcript=None,
        summary=None,
        full_text=None,
        folder=None,
        tags=None,
    ):
        self.execute("""
            UPDATE notes
            SET title = COALESCE(?, title),
                transcript = COALESCE(?, transcript),
                summary = COALESCE(?, summary),
                full_text = COALESCE(?, full_text),
                folder = COALESCE(?, folder),
                tags = COALESCE(?, tags),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (title, transcript, summary, full_text, folder, tags, note_id))

    def delete_note(self, note_id):
        self.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    # ---------- MEMORY ----------

    def set_memory(self, key, value):
        self.execute("""
            INSERT INTO memory (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (key, value))

    def get_memory(self, key):
        row = self.fetchone("SELECT value FROM memory WHERE key = ?", (key,))
        return row["value"] if row else None

    # ---------- EMBEDDINGS ----------

    def add_embedding(self, note_id, vector):
        self.execute("""
            INSERT INTO embeddings (note_id, vector)
            VALUES (?, ?)
            ON CONFLICT(note_id) DO UPDATE SET
                vector = excluded.vector
        """, (note_id, vector))

    def get_embedding(self, note_id):
        return self.fetchone("SELECT vector FROM embeddings WHERE note_id = ?", (note_id,))

    # ---------- USER ----------

    def set_user(self, name=None, preferences=None):
        self.execute("""
            INSERT INTO user (id, name, preferences)
            VALUES (1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = COALESCE(?, name),
                preferences = COALESCE(?, preferences)
        """, (name, preferences, name, preferences))

    def get_user(self):
        return self.fetchone("SELECT * FROM user WHERE id = 1")

    # ---------- CLEANUP ----------

    def close(self):
        pass