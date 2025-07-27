from utils.db_manager import initialize_db
import sounddevice as sd
from scipy.io.wavfile import write
from utils.transcriber import transcribe_audio
from utils.db_manager import Note
from pipeline.save_note import save_new_note
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from pathlib import Path

DEBUG = True

Builder.load_file("ui/layout.kv")

class MainLayout(BoxLayout):
    def record_note(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio/note_{timestamp}.wav"
        
        record_voice(filename)
        transcription = transcribe_audio(filename)
        result = save_new_note(note_text=transcription, audio_path=filename)
        self.ids.notes_label.text = f"{transcription}\n\n→ Saved to: {result['folder_path']}"

class LifenotesApp(App):
    def build(self):
        initialize_db()
        return MainLayout()


def record_voice(filename, duration=5, samplerate=16000):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    if DEBUG:
        print("Recording... (record_voice)")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, recording)
    if DEBUG:
        print("Saved:", filename)


def main():
    pass


if __name__ == "__main__":
    LifenotesApp().run()
    main()