import streamlit as st
import uuid
from datetime import datetime, timezone
from pathlib import Path



def render_kahnban():
    st.title("Kahn Ban")
    st.selectbox("Board", )

class KBFile:
    def __init__(self):
        self.path = "boards.txt"
        self.boards = []

    def load(self):
        boards_file = Path(self.path).read_text(encoding="utf-8")
        for board in boards_file:
            pass

    def save(self, board):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(f"""
                
            """)


        

class Board:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.bins = {
            "Backlog": Bin("Backlog"),
            "Active": Bin("Active"),
            "Review": Bin("Review"),
            "Done": Bin("Done")
        }

class Bin:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.tasks = []

class Task:
    def __init__(self, name: str, priority: int, deadline: datetime, important: bool, urgent: bool):
        self.id = str(uuid.uuid4())
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.important = important
        self.urgent = urgent