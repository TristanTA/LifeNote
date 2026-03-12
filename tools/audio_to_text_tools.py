from instances.audio_to_text_instance import audio_to_text
from langchain.tools import tool

@tool
def transcribe_audio(audio_file:str) -> str:
    """
    Transcribe an audio file
    Args: audio_file: str - The file path of the audio
    Returns: str - Transcription
    """
    print(f"[TOOLS] Transcribing audio file: {audio_file}")
    transcription = audio_to_text.transcribe(audio_file)
    return transcription