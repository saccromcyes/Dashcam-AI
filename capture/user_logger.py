import os
import json
from datetime import datetime

# Create log directory if it doesn't exist
LOG_DIR = r"data/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "session_log.json")

# Initialize the JSON file if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

def log_event(event_type, description):
    """
    Logs a single event (like 'screen_event' or 'audio_transcript')
    into data/logs/session_log.json with timestamp.
    """

    event = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "description": description
    }

    try:
        # Read existing logs
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

        # Append the new event
        logs.append(event)

        # Write updated logs
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

        print(f"[LOGGED] {event_type}: {description}")

    except Exception as e:
        print(f"[ERROR] Could not write to log: {e}")

def show_latest_logs(limit=5):
    """Prints the last few logs for quick debugging."""
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        print("\n--- Recent Logs ---")
        for log in logs[-limit:]:
            print(f"{log['timestamp']} | {log['type']} | {log['description']}")
        print("--------------------\n")
    except Exception as e:
        print(f"[ERROR] Could not read log file: {e}")

if __name__ == "__main__":
    print("User Logger started...")

    # Example logs for testing
    log_event("screen_event", "User opened Notepad and typed 'Hello World'")
    log_event("audio_transcript", "User said 'save report to desktop'")
    log_event("ocr_text", "Detected text 'Excel report Q4'")
    
    show_latest_logs()
    print(f"Session log saved at: {LOG_FILE}")
