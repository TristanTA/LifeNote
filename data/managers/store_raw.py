import sqlite3
import pandas as pd
import json

from data.schemas.session_schema import Session
from data.schemas.text_schema import Text

class RawData:
    def __init__(self, file_path: str = "data/raw/raw_data.db"):
        self.file_path = file_path
        self.conn = sqlite3.connect(self.file_path)
        self._create_table()
        self.df = self._load_to_dataframe()
    
    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    text TEXT
                )
            """)

    def _load_to_dataframe(self):
        try:
            return pd.read_sql_query("SELECT * FROM notes", self.conn)
        except Exception:
            return pd.DataFrame(columns=["id", "timestamp", "text"])

    def store_session(self, session_obj: Session):
        # Serialize list of Text objects → list of dicts → JSON string
        serialized_text = json.dumps(
            [vars(t) for t in session_obj.text], default=str
        )

        with self.conn:
            self.conn.execute(
                "INSERT INTO notes (id, timestamp, text) VALUES (?, ?, ?)",
                (session_obj.id, session_obj.timestamp.isoformat(), serialized_text)
            )

        new_row = {
            "id": session_obj.id,
            "timestamp": session_obj.timestamp.isoformat(),
            "text": serialized_text
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def get_dataframe(self):
        return self.df

    def close(self):
        self.conn.close()
    
    def get_sessions(self):
        df = self.get_dataframe()
        sessions = []
        for _, row in df.iterrows():
            text_objs = [Text(**json.loads(t)) for t in json.loads(row["text"])]
            sessions.append(Session(text_objs))
        return sessions