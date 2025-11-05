# recorder.py
import av
import wave
import numpy as np
from streamlit_webrtc import AudioProcessorBase

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.frames = []
        self.volume_level = 0.0
        self.frame_count = 0

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        try:
            audio = frame.to_ndarray()
            self.frame_count += 1

            # Debug print for every 30 frames (to reduce spam)
            if self.frame_count % 30 == 0:
                print(f"[AudioRecorder] ✅ Received {self.frame_count} frames so far.")

            if audio.size > 0:
                self.volume_level = float(np.sqrt(np.mean(audio ** 2)))
            else:
                print("[AudioRecorder] ⚠️ Empty audio frame received.")

            self.frames.append(audio)
        except Exception as e:
            print(f"[AudioRecorder] ❌ Error converting frame: {e}")

        return frame

    def save_wav(self, filename="audio_debug.wav"):
        print(f"[AudioRecorder] Attempting to save {len(self.frames)} frames...")
        if not self.frames:
            print("[AudioRecorder] ❌ No frames captured — nothing to save.")
            return None

        try:
            audio_data = np.concatenate(self.frames, axis=1)
            if audio_data.dtype != np.int16:
                audio_data = (audio_data * 32767).astype(np.int16)

            with wave.open(filename, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_data.tobytes())

            print(f"[AudioRecorder] ✅ Saved audio to {filename}")
            return filename
        except Exception as e:
            print(f"[AudioRecorder] ❌ Error writing WAV: {e}")
            return None
