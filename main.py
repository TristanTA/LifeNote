from utils.db_manager import initialize_db
import sounddevice as sd
from scipy.io.wavfile import write
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os

Builder.load_file("ui/layout.kv")

class MainLayout(BoxLayout):
    def record_note(self):
        print("Starting recording...")

class LifenotesApp(App):
    def build(self):
        return MainLayout()


def record_voice(filename, duration=5, samplerate=16000):
    print("Recording...")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, recording)
    print("Saved:", filename)


def main():
    initialize_db()


if __name__ == "__main__":
    LifenotesApp().run()
    main()