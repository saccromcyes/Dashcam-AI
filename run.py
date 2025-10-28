import os
import time
from datetime import datetime

# --- Capture Modules ---
from capture.screenshot_capture import capture_screenshots
from capture.audio_capture import capture_audio
from capture.speech_recognition import transcribe_audio
from capture.ocr import extract_text_from_images
from capture.user_logger import log_event

# --- Analysis Modules ---
from analysis.summarizer import summarize_session
from analysis.pattern_detector import detect_patterns


def main():
    print("\n Starting Dashcam AI session...\n")

    # Ensure all directories exist
    os.makedirs("data/screenshots", exist_ok=True)
    os.makedirs("data/audio", exist_ok=True)
    os.makedirs("data/logs", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # Capture screenshot(s)
    print("Capturing screenshot...")
    screenshot_paths = capture_screenshots()
    print(f"Captured {len(screenshot_paths)} screenshots.\n")

    # OCR extraction
    print("Running OCR on captured image...")
    ocr_results = extract_text_from_images(screenshot_paths)

    # Safely join extracted text
    if ocr_results:
        ocr_text_combined = "\n".join([item["extracted_text"] for item in ocr_results if item["extracted_text"]])
    else:
        ocr_text_combined = ""
    print("OCR text extracted.\n")


    # Record audio
    print("Recording audio (please speak clearly)...")
    audio_path = capture_audio(duration=10)
    print(f"Audio recorded: {audio_path}\n")

    # Speech-to-text transcription
    print("Transcribing audio...")
    transcript_path = transcribe_audio(audio_path)
    transcript_text = ""
    if transcript_path and os.path.exists(transcript_path):
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_text = f.read().strip()
    print(f"Transcription complete: {transcript_path}\n")
 
    # STEP Combine OCR + Speech logs
    print("Logging OCR + Speech data...")
    log_event("ocr_text", ocr_text_combined if ocr_text_combined else "No text detected from OCR.")
    log_event("speech_text", transcript_text if transcript_text else "No speech detected.")
    session_log = os.path.join("data", "logs", "session_log.json")
    print(f"User session log created at: {session_log}\n")

    # Summarization
    print("Summarizing session...")
    summary_path = summarize_session(transcript_text + "\n\n" + ocr_text_combined)
    print(f"Summary generated at: {summary_path}\n")

    # Pattern Detection
    print("Detecting patterns and behavior insights...")
    pattern_report = detect_patterns(summary_path)
    print(f"Pattern detection complete: {pattern_report}\n")

    # DONE
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n Dashcam AI session completed at {timestamp}")
    print("\n Check the 'output/' folder for:")
    print("   - transcript.txt")
    print("   - session_summary.txt")
    print("   - suggestions.txt")
    print("   - pattern_report.txt\n")
    time.sleep(1)


if __name__ == "__main__":
    main()
