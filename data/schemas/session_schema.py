import uuid
from datetime import datetime, timezone
import json

from data.schemas.text_schema import Text

class Session:
    def __init__(self, text: list[Text]):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now(timezone.utc)
        self.text = text

    def add_text(self, text_obj: Text):
        self.text.append(text_obj)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "text": [t.to_dict() for t in self.text]
        }