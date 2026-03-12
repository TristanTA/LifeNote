from models.summarizer import Summarizer
from instances.db_instance import db
from inputs.debug import get_debug_note

db.create_input(
    input_type="text",
    content_text=get_debug_note()
)

db.create_input(
    input_type="audio",
    file_path="samples/sample_audio.m4a"
)

sum = Summarizer()
response = sum.invoke()
print(response)