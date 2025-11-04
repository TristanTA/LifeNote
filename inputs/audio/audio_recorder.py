from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av
import wave
import numpy as np
import os

AUDIO_FILE = "audio.wav"

class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert audio frame to numpy
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame

    def save_wav(self, filename=AUDIO_FILE):
        if not self.frames:
            return None

        # Convert list of frames to one numpy array
        audio_data = np.concatenate(self.frames, axis=1)

        # Convert float32 to int16 if needed
        if audio_data.dtype != np.int16:
            audio_data = (audio_data * 32767).astype(np.int16)

        # Write to WAV file
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes = 16-bit
            wf.setframerate(16000)  # typical mic sample rate
            wf.writeframes(audio_data.tobytes())

        return filename
