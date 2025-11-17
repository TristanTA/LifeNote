import uuid
from datetime import datetime, timezone

from data.schemas.text_schema import Text

class Session:
    def __init__(self, text: list[Text]):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now(timezone.utc)
        self.text: list[Text] = text

    def add_text(self, text: Text):
        self.text.append(text)

    def get_all(self):
        package = (
            {
                "id": self.id,
                "timestamp": self.timestamp.isoformat(),
                "text": [t.get_all() for t in self.text],
            }
        )
        return package