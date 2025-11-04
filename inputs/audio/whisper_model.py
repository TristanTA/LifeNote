from faster_whisper import WhisperModel

def transcribe_audio(file):
    model = WhisperModel("base", device="cpu")
    segments, info = model.transcribe(file)

    text = ""
    for segment in segments:
        text += segment.text + " "
    
    return text.strip()