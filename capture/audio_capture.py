import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os, datetime

def capture_audio(duration=5, samplerate=44100, device_index=None):
    os.makedirs("data/audio", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/audio/audio_{timestamp}.wav"

    if device_index is not None:
        sd.default.device = (device_index, None)

    print(f"Recording from: {sd.query_devices()[sd.default.device[0]]['name']}")
    print(f"Recording for {duration} seconds...")

    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete!")

    # --- Normalize Audio ---
    recording = recording.astype(np.float32)
    max_val = np.max(np.abs(recording))
    if max_val > 0:
        recording = recording / max_val * 32767  # scale to full 16-bit range
    recording = recording.astype(np.int16)

    write(filename, samplerate, recording)
    print(f"Saved (normalized) audio at: {filename}")

    return filename

if __name__ == "__main__":
    capture_audio(duration=5, samplerate=44100, device_index=1)
