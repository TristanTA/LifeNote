from datetime import datetime, timezone
import uuid

class TextInput:
    def __init__(self, content: str):
        self.id: int = int(uuid.uuid4())
        self.timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        self.content: str = content