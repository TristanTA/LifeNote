from utils.db_manager import initialize_db
import sounddevice as sd
from scipy.io.wavfile import write
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os

DEBUG = True

Builder.load_file("ui/layout.kv")

class MainLayout(BoxLayout):
    def record_note(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio/note_{timestamp}.wav"
        record_voice(filename)

class LifenotesApp(App):
    def build(self):
        initialize_db
        return MainLayout()


def record_voice(filename, duration=5, samplerate=16000):
    if DEBUG:
        print("Recording...")
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