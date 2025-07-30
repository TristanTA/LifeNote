from utils.db_manager import initialize_db
from utils.transcriber import transcribe_audio
from utils.db_manager import Note
from pipeline.save_note import save_new_note

from datetime import datetime
from pathlib import Path
import sounddevice as sd
from scipy.io.wavfile import write

from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

DEBUG = True

# Load the updated multi-screen KV layout
Builder.load_file("ui/layout.kv")

class LifenotesApp(MDApp):
    def build(self):
        initialize_db()
        return self.root  # The root is set by the KV file (MDNavigationLayout)

    def toggle_recording(self):
        """Triggered when the mic icon is pressed."""
        self.start_recording_animation()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio/note_{timestamp}.wav"
        
        # Start audio recording in a thread-safe way
        def record_and_save(_):
            record_voice(filename)
            transcription = transcribe_audio(filename)
            result = save_new_note(note_text=transcription, audio_path=filename)

            # Update the UI (must be scheduled on the main thread)
            def update_label(dt):
                self.root.ids.input_text.text = ""  # Clear input
                self.root.ids.screen_manager.get_screen("main").ids.input_text.text = ""
                self.root.ids.screen_manager.get_screen("main").ids.mic_icon.text_color = (1, 1, 1, 1)
                self.root.ids.screen_manager.get_screen("main").ids.mic_icon.user_font_size = "72sp"
                self.root.ids.screen_manager.get_screen("main").ids.mic_icon.icon = "microphone"
                self.root.ids.screen_manager.get_screen("main").ids.input_text.hint_text = f"{transcription[:50]}..."
            Clock.schedule_once(update_label)

        Clock.schedule_once(record_and_save, 0)  # async wrapper
        Clock.schedule_once(lambda dt: self.stop_recording_animation(), 5)

    def send_text_note(self):
        """Triggered when the Send button is pressed."""
        text = self.root.ids.screen_manager.get_screen("main").ids.input_text.text.strip()
        if not text:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fake_audio_path = f"audio/note_{timestamp}.wav"

        result = save_new_note(note_text=text, audio_path=None)
        if DEBUG:
            print("Text note saved:", result)

        self.root.ids.screen_manager.get_screen("main").ids.input_text.text = ""
        self.root.ids.screen_manager.get_screen("main").ids.input_text.hint_text = "Note saved!"

    def start_recording_animation(self):
        mic = self.root.ids.screen_manager.get_screen("main").ids.mic_icon
        self.anim = Animation(user_font_size="80sp", text_color=(1, 0, 0, 1), duration=0.5) + \
                    Animation(user_font_size="72sp", text_color=(1, 1, 1, 1), duration=0.5)
        self.anim.repeat = True
        self.anim.start(mic)

    def stop_recording_animation(self):
        mic = self.root.ids.screen_manager.get_screen("main").ids.mic_icon
        if hasattr(self, 'anim'):
            self.anim.cancel(mic)
        mic.user_font_size = "72sp"
        mic.text_color = (1, 1, 1, 1)

def record_voice(filename, duration=5, samplerate=16000):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    if DEBUG:
        print("Recording... (record_voice)")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, recording)
    if DEBUG:
        print("Saved:", filename)

if __name__ == "__main__":
    LifenotesApp().run()