import uuid
from datetime import datetime, timezone
import json

class Text:
    def __init__(self, content: dict):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now(timezone.utc)
        self.content = content
        self.tags = []
        self.title = ""

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "content": self.content,
            "tags": self.tags,
            "title": self.title
        }
