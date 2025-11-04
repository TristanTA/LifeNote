import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from inputs.audio.whisper_model import transcribe_audio
from schemas.text_class import TextInput
from inputs.audio.audio_recorder import AudioRecorder

def display_audio_ui():
    st.title("Record Audio")

    recorder = AudioRecorder()

    ctx = webrtc_streamer(
        key="audio",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        audio_processor_factory=lambda: recorder,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.state.playing:
        if st.button("Stop & Save"):
            filename = recorder.save_wav()
            if filename:
                st.success(f"Audio saved to {filename}")
                output_text = transcribe_audio(filename)
            else:
                st.warning("No audio frames captured yet.")
    return output_text if 'output_text' in locals() else ""