import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from inputs.audio.recorder import AudioRecorder
from inputs.audio.whisper_model import transcribe_audio
import os, time

def dummy_video_frame_callback(frame):
    return frame

def display_audio_ui():
    st.title("🎙 Audio Debug Mode")

    st.info("This view prints connection and frame-level info to your terminal.")
    st.text(f"Current working dir: {os.getcwd()}")

    ctx = webrtc_streamer(
        key="audio",
        mode=WebRtcMode.SENDRECV,
        audio_receiver_size=256,
        audio_processor_factory=AudioRecorder,
        video_frame_callback=dummy_video_frame_callback,
        media_stream_constraints={
            "audio": {
                "echoCancellation": True,
                "noiseSuppression": True,
                "autoGainControl": True,
            },
            "video": False,
        },
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
    )

    # Show basic connection state
    st.write("### Connection state:")
    st.json({
        "ctx.state.playing": ctx.state.playing,
        "ctx.audio_processor exists": ctx.audio_processor is not None,
        "ctx.audio_receiver exists": ctx.audio_receiver is not None,
    })

    if "recorded" not in st.session_state:
        st.session_state.recorded = False

    # --- When active ---
    if ctx.state.playing and ctx.audio_processor:
        st.success("🟢 Recording Active — Speak into your mic")
        progress_bar = st.progress(0)
        status = st.empty()
        count_display = st.empty()

        while ctx.state.playing:
            vol = ctx.audio_processor.volume_level
            count_display.write(f"Frames captured: {ctx.audio_processor.frame_count}")
            progress_bar.progress(int(min(vol * 100, 100)))
            time.sleep(0.1)

        progress_bar.empty()
        status.empty()
        count_display.empty()

    # --- When stopped ---
    elif not ctx.state.playing and not st.session_state.recorded:
        st.warning("🟠 Stream stopped — finalizing audio.")
        recorder = getattr(ctx, "audio_processor", None)
        if recorder:
            print("[UI] Saving audio after stop event...")
            save_name = os.path.join(os.getcwd(), f"audio_debug_{time.strftime('%H%M%S')}.wav")
            filename = recorder.save_wav(save_name)
            if filename and os.path.exists(filename):
                st.success(f"✅ Saved audio file: {filename}")
                try:
                    text = transcribe_audio(filename)
                    st.write("**Transcription:**", text)
                except Exception as e:
                    st.error(f"❌ Whisper failed: {e}")
            else:
                st.error("❌ No file written; frames may be empty.")
        else:
            st.error("❌ ctx.audio_processor is None (stream destroyed early).")

        st.session_state.recorded = True

    return ""
