from utils.db_manager import initialize_db, Note
from utils.transcriber import transcribe_audio
from pipeline.save_note import save_new_note
from utils.json_manager import load_folder_index

from datetime import datetime
from pathlib import Path
import sounddevice as sd
from scipy.io.wavfile import write, read

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

DEBUG = True
Builder.load_file("ui/layout.kv")


class LifenotesApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_data = None
        self.audio_fs = None
        self.audio_stream = None
        self.playback_clock = None
        self.current_time = 0
        self.total_time = 0
        self.playing_note = None

    def build(self):
        initialize_db()
        return self.root

    def on_start(self):
        Clock.schedule_once(lambda dt: self.load_recent_notes(), 1)

        screen_manager = self.root.ids.screen_manager
        notes_screen = screen_manager.get_screen("notes")

        if hasattr(notes_screen, 'on_pre_enter'):
            notes_screen.bind(on_pre_enter=lambda *_: self.load_recent_notes())

        tabs = notes_screen.ids.notes_tabs
        tabs.bind(on_tab_switch=self.on_tab_switch)

    # ====================== Recording ======================
    def toggle_recording(self):
        self.start_recording_animation()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio/note_{timestamp}.wav"

        def record_and_save(_):
            record_voice(filename)
            transcription = transcribe_audio(filename)
            result = save_new_note(note_text=transcription, audio_path=filename)

            def update_label(dt):
                self.root.ids.screen_manager.get_screen("main").ids.input_text.text = ""
                self.root.ids.screen_manager.get_screen("main").ids.input_text.hint_text = f"{transcription[:50]}..."
                self.reset_mic_icon()

            Clock.schedule_once(update_label)

        Clock.schedule_once(record_and_save, 0)
        Clock.schedule_once(lambda dt: self.stop_recording_animation(), 5)

    def send_text_note(self):
        text_input = self.root.ids.screen_manager.get_screen("main").ids.input_text
        text = text_input.text.strip()
        if not text:
            return

        save_new_note(note_text=text, audio_path=None)
        text_input.text = ""
        text_input.hint_text = "Note saved!"

    def start_recording_animation(self):
        mic = self.root.ids.screen_manager.get_screen("main").ids.mic_icon
        self.anim = Animation(user_font_size="80sp", text_color=(1, 0, 0, 1), duration=0.5) + \
                    Animation(user_font_size="72sp", text_color=(1, 1, 1, 1), duration=0.5)
        self.anim.repeat = True
        self.anim.start(mic)

    def stop_recording_animation(self):
        if hasattr(self, 'anim'):
            mic = self.root.ids.screen_manager.get_screen("main").ids.mic_icon
            self.anim.cancel(mic)
            self.reset_mic_icon()

    def reset_mic_icon(self):
        mic = self.root.ids.screen_manager.get_screen("main").ids.mic_icon
        mic.user_font_size = "72sp"
        mic.text_color = (1, 1, 1, 1)

    # ====================== Notes ======================
    def load_recent_notes(self):
        notes_grid = self.root.ids.screen_manager.get_screen("notes").ids.notes_grid
        notes_grid.clear_widgets()

        self.all_notes = list(Note.select().order_by(Note.created_at.desc()).limit(50))

        if not self.all_notes:
            notes_grid.add_widget(
                MDLabel(
                    text="No notes found. Try recording or typing one!",
                    halign="center",
                    theme_text_color="Hint",
                    size_hint_y=None,
                    height="48dp"
                )
            )
            return

        for note in self.all_notes:
            self.add_note_card(note, notes_grid)

    def add_note_card(self, note, parent_grid):
        card = MDCard(
            orientation="vertical",
            padding="12dp",
            radius=[12, 12, 12, 12],
            size_hint=(1, None),
            height="140dp",
            elevation=3,
            ripple_behavior=True,
            on_release=lambda n=note: self.open_note_detail(n)
        )

        layout = BoxLayout(orientation="vertical", padding=(8, 4), spacing=4)
        layout.add_widget(MDLabel(text=note.content[:100] + "...", theme_text_color="Primary", font_style="Body1"))
        layout.add_widget(MDLabel(text=f"📁 {note.folder_path}", font_style="Caption", theme_text_color="Hint"))
        card.add_widget(layout)

        parent_grid.add_widget(card)

    def open_note_detail(self, note):
        self.stop_audio_playback()

        content = BoxLayout(orientation="vertical", padding="8dp", spacing="10dp")
        content.add_widget(MDLabel(text=note.content, theme_text_color="Primary"))

        self.dialog = MDDialog(
            title=note.folder_path or "Note",
            type="custom",
            content_cls=content,
            buttons=[],
            auto_dismiss=True
        )
        self.dialog.open()

        # Preload audio if available (no autoplay)
        if note.audio_path and Path(note.audio_path).exists():
            data, fs = read(note.audio_path, dtype='float32')
            self.audio_data = data
            self.audio_fs = fs
            self.playing_note = note
            self.current_time = 0
            self.total_time = int(len(data) / fs)

            self.root.ids.audio_slider.max = self.total_time
            self.root.ids.audio_slider.value = 0
            self.root.ids.audio_time.text = f"0:00 / {self.format_time(self.total_time)}"
            self.root.ids.audio_play_pause.icon = "play"
            self.root.ids.audio_player.opacity = 1

    # ====================== Playback ======================
    def toggle_audio_playback(self):
        if not self.audio_data:
            return

        if self.audio_stream and self.audio_stream.active:
            sd.stop()
            self.audio_stream.stop()
            self.root.ids.audio_play_pause.icon = "play"
        else:
            sd.play(self.audio_data[self.current_time * self.audio_fs:], self.audio_fs)
            self.root.ids.audio_play_pause.icon = "pause"
            self.playback_clock = Clock.schedule_interval(self.update_playback_progress, 1)

    def stop_audio_playback(self):
        if self.audio_stream:
            sd.stop()
            self.audio_stream.stop()
            self.audio_stream.close()
            self.audio_stream = None
        if self.playback_clock:
            self.playback_clock.cancel()
            self.playback_clock = None
        self.root.ids.audio_play_pause.icon = "play"
        self.root.ids.audio_slider.value = 0
        self.root.ids.audio_time.text = "0:00 / 0:00"
        self.root.ids.audio_player.opacity = 0

    def update_playback_progress(self, dt):
        self.current_time += 1
        if self.current_time >= self.total_time:
            self.stop_audio_playback()
            return
        self.root.ids.audio_slider.value = self.current_time
        self.root.ids.audio_time.text = f"{self.format_time(self.current_time)} / {self.format_time(self.total_time)}"

    def scrub_audio(self, instance, touch):
        slider = self.root.ids.audio_slider
        if slider.collide_point(*touch.pos) and self.audio_data:
            self.current_time = int(slider.value)
            sd.stop()
            sd.play(self.audio_data[self.current_time * self.audio_fs:], self.audio_fs)
            self.root.ids.audio_play_pause.icon = "pause"

    @staticmethod
    def format_time(seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}:{s:02}"

    # ====================== Filtering ======================
    def filter_notes(self, query):
        notes_grid = self.root.ids.screen_manager.get_screen("notes").ids.notes_grid
        notes_grid.clear_widgets()

        if not query.strip():
            notes = self.all_notes[:10]
        else:
            q = query.lower()
            notes = [n for n in self.all_notes if
                     q in n.content.lower() or
                     q in (n.tags or "").lower() or
                     q in (n.folder_path or "").lower()]

        if not notes:
            notes_grid.add_widget(MDLabel(text="No matching notes found.", halign="center", theme_text_color="Hint"))
            return

        for note in notes:
            self.add_note_card(note, notes_grid)

    # ====================== Folders ======================
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "Folders":
            self.load_folders()

    def load_folders(self):
        folder_list = self.root.ids.screen_manager.get_screen("notes").ids.folder_list
        folder_list.clear_widgets()

        index = load_folder_index()
        for folder in index:
            item = OneLineAvatarIconListItem(
                text=folder,
                on_release=lambda x, f=folder: self.open_folder(f)
            )
            item.add_widget(IconLeftWidget(icon="folder"))
            folder_list.add_widget(item)

    def open_folder(self, folder_name):
        index = load_folder_index()
        notes = index.get(folder_name, [])

        content = BoxLayout(orientation="vertical", spacing="8dp", padding="8dp")
        scroll = ScrollView()
        inner = BoxLayout(orientation="vertical", size_hint_y=None)
        inner.bind(minimum_height=inner.setter("height"))

        if not notes:
            inner.add_widget(MDLabel(text="No notes in this folder.", halign="center"))
        else:
            for entry in notes:
                label = MDLabel(
                    text=f"• {entry['title']}",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height="36dp"
                )
                inner.add_widget(label)

        scroll.add_widget(inner)
        content.add_widget(scroll)

        self.dialog = MDDialog(title=folder_name, type="custom", content_cls=content)
        self.dialog.open()


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