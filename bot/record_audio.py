import sounddevice as sd
from scipy.io.wavfile import write
import os
from dotenv import load_dotenv

load_dotenv()

class AudioRecorder:
    def __init__(self):
        self.sample_rate = int(os.getenv('SAMPLE_RATE', 44100))
        self.filename = None
        self.recording = None

    def start_recording(self, filename, duration):
        print("Recording...")
        self.filename = filename
        self.recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=2, dtype='int16')

    def stop_recording(self):
        sd.stop()
        write(self.filename, self.sample_rate, self.recording)
        print(f"Recording finished. Saved as {self.filename}.")
