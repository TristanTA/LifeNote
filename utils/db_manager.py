from peewee import *

db = SqliteDatabase('db/notes.db')

class Note(Model):
    content = TextField()
    audio_path = TextField()
    created_at = DateTimeField()
    folder_path = TextField(null=True)
    tags = TextField(null=True)

    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Note], safe=True)
