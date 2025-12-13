import streamlit as st
import uuid
from datetime import datetime, timezone
from pathlib import Path



def render_kahnban():
    st.title("Kahn Ban")
    st.selectbox("Board")

class KahnbanApp:
    def __init__(self):
        self.path = Path("boards.txt")
        self.boards = []
        self.bins = []
        self.tasks = []

    def load(self):
        if self.path.exists():
            with open(self.path, "r") as f:
                data = f.read()
                
    
    def save(self):
        with open(self.path, "w") as f:
            for board in self.boards:
                f.write(f"Board: {board.name} (ID: {board.id})\n")
                for bin in board.bins:
                    f.write(f"Bin: {bin.name} (ID: {bin.id})\n")
                    for task in bin.tasks:
                        f.write(f"Task: {task.name} (ID: {task.id}, Priority: {task.priority}, Deadline: {task.deadline}, Important: {task.important}, Urgent: {task.urgent})\n")

class Board:
    def __init__(self, app: KahnbanApp, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.bins = [Bin(app, "Backlog", self), Bin(app, "Active", self), Bin(app, "Review", self), Bin(app, "Done", self)]

        app.boards.append(self)

class Bin:
    def __init__(self, app: KahnbanApp, name: str, target_board: Board):
        self.id = str(uuid.uuid4())
        self.name = name
        self.board = target_board
        self.tasks = []

        app.bins.append(self)

class Task:
    def __init__(self, app: KahnbanApp, name: str, target_bin: Bin, priority: int, deadline: datetime, important: bool, urgent: bool):
        self.id = str(uuid.uuid4())
        self.bin = target_bin
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.important = important
        self.urgent = urgent

        target_bin.tasks.append(self)
        app.tasks.append(self)