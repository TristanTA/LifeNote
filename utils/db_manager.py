from peewee import *

db = SqliteDatabase('db/notes.db')

class Note(Model):
    content = TextField()
    audio_path = TextField()
    created_at = DateTimeField()

    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Note], safe=True)
