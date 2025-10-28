import os
import wave
import json
from vosk import Model, KaldiRecognizer
from .user_logger import log_event  #Import your logger

def transcribe_audio(audio_path="data/audio/audio.wav"):
    # Path to Vosk model
    model_path = r"C:\Users\ndsha\Desktop\New folder (4)\model\vosk-model"
    if not os.path.exists(model_path):
        raise FileNotFoundError("Vosk model not found! Place it inside models/vosk-model/")

    # Open audio file
    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [16000, 44100]:
        raise ValueError("Audio file must be WAV mono PCM with 16- or 44.1-kHz sample rate")

    # Load model and recognizer
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # Process audio in chunks
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))

    # Final result
    results.append(json.loads(rec.FinalResult()))

    # Combine all text segments
    text_output = " ".join([r.get("text", "") for r in results]).strip()

    # Save transcript
    os.makedirs("output", exist_ok=True)
    output_path = "output/transcript.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text_output)

    # Log this event for pattern recognition
    log_event("speech_text", text_output)

    print(f"Transcription saved to {output_path}")
    return text_output


if __name__ == "__main__":
    audio_file = r"C:\Users\ndsha\Desktop\New folder (4)\data\audio\audio_20251023_225314.wav"  # change to your latest .wav file
    print("Transcribing...")
    text = transcribe_audio(audio_file)
    print("\n Transcribed Text:\n", text)
