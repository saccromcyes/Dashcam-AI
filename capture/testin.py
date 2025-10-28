import sounddevice as sd
from scipy.io.wavfile import write
import sys

# Ensure emojis or special text print correctly
sys.stdout.reconfigure(encoding='utf-8')

print("Available audio input devices:\n")
devices = sd.query_devices()
9
# List only input-capable devices
input_devices = []
for i, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        input_devices.append(i)
        print(f"{i}: {device['name']}")

# Ask user to select one
device_index = int(input("\nEnter the device number you want to use for recording: "))

# Record settings
samplerate = int(sd.query_devices(device_index)['default_samplerate']) # Sample rate (Hz)
duration = 20      # Duration in seconds
filename = "mic1_test.wav"

print(f"\nUsing device {device_index}: {sd.query_devices()[device_index]['name']}")
print("Recording test... say something!")

# Record
audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16', device=device_index)
sd.wait()

# Save file
write(filename, samplerate, audio)

print(f"\nRecording finished. Saved as '{filename}' in the same folder as this script.")
