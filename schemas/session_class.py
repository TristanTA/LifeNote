import uuid

from schemas.text_class import TextInput

class Session:
    def __init__(self):
        self.session_id: int = int(uuid.uuid4())
        self.text_inputs: list[TextInput] = []