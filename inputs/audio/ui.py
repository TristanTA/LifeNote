import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from inputs.audio.whisper_model import transcribe_audio
from schemas.text_class import TextInput
from inputs.audio.audio_recorder import AudioRecorder

def display_audio_ui():
    st.title("Record Audio")

    ctx = webrtc_streamer(
        key="audio",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=256,
        audio_processor_factory=AudioRecorder,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.state.playing and ctx.audio_processor:
        if st.button("Stop & Save"):
            recorder = ctx.audio_processor
            filename = recorder.save_wav()
            if filename:
                st.success(f"Audio saved to {filename}")
                text = transcribe_audio(filename)
                st.subheader("Transcribed text:")
                st.write(text)
            else:
                st.warning("No audio frames captured yet.")
    return text if 'text' in locals() else ""