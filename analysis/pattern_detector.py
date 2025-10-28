import os
import json
import re
from collections import Counter

def detect_patterns(summary_path=None):
    output_folder = "output"
    summaries = []

    # Collect all previous session summaries
    for file in os.listdir(output_folder):
        if file.startswith("session_summary") and file.endswith(".txt"):
            with open(os.path.join(output_folder, file), "r", encoding="utf-8") as f:
                summaries.append(f.read().lower())

    # If a specific summary file path is provided, include that too
    if summary_path and os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summaries.append(f.read().lower())

    if not summaries:
        print("No summaries found for pattern detection.")
        return

    # Combine all text
    combined_text = " ".join(summaries)

    # Common keywords that represent user actions
    action_keywords = ["open", "save", "click", "type", "search", "download", "upload", "move", "rename", "copy"]

    # Find matches in text
    found_actions = []
    for keyword in action_keywords:
        matches = re.findall(rf"\b{keyword}\b.*?\b\w+\b", combined_text)
        found_actions.extend(matches)

    # Count repetitions
    action_counts = Counter(found_actions)
    repeated_actions = {k: v for k, v in action_counts.items() if v > 1}

    # Generate automation suggestions
    suggestions = []
    for action, count in repeated_actions.items():
        suggestions.append(f"Repeated action detected: '{action}' occurred {count} times — can be automated.")

    # Save to JSON
    pattern_data = {
        "patterns": repeated_actions,
        "automation_suggestions": suggestions
    }

    os.makedirs("output", exist_ok=True)
    with open("output/patterns.json", "w", encoding="utf-8") as f:
        json.dump(pattern_data, f, indent=4)

    print("\nPattern Detection Complete!")
    print(f"Found {len(repeated_actions)} repetitive actions.")
    print("Automation suggestions saved to: output/patterns.json\n")

    if suggestions:
        for s in suggestions:
            print("", s)
    else:
        print("No repetitive actions yet — use the assistant more to teach it your habits!")

if __name__ == "__main__":
    detect_patterns()
