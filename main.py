from utils.db_manager import initialize_db
import sounddevice as sd
from scipy.io.wavfile import write
import datetime
import os

def record_voice(filename, duration=5, samplerate=16000):
    print("Recording...")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    write(filename, samplerate, recording)
    print("Saved:", filename)


def main():
    initialize_db()



if __name__ == "__main__":
    main()