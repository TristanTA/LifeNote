import uuid
from datetime import datetime, timezone

class Text:
    def __init__(self, content: str):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now(timezone.utc)
        self.content = content
        self.tags = []
        self.title = ""