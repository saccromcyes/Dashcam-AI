import subprocess
import os
import sys

# Ensure UTF-8 output
os.environ["PYTHONIOENCODING"] = "utf-8"

# File paths
TRANSCRIPT_PATH = r"output/transcript.txt"
SUMMARY_PATH = r"output/session_summary.txt"
SUGGESTIONS_PATH = r"output/suggestions.txt"


def run_llm(prompt: str) -> str:
    """
    Run Ollama llama3 safely (UTF-8 safe, with timeout).
    """
    try:
        result = subprocess.run(
            [r"C:\Users\ndsha\AppData\Local\Programs\Ollama\ollama.exe", "run", "llama3"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180  # 3 minutes max
        )

        if result.returncode != 0:
            print("Ollama returned an error:", result.stderr.strip())
            return "Error running Ollama."

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print("Timeout: Ollama took too long to respond.")
        return "Summarization timed out."

    except FileNotFoundError:
        print("Ollama not found. Please install it and add to PATH.")
        return "Ollama not found."


def summarize_session(transcript_text=None):
    """
    Summarizes transcript and generates suggestions.
    Can be run directly OR called from another script with transcript_text.
    """
    # --- Load transcript ---
    if transcript_text is None:
        if not os.path.exists(TRANSCRIPT_PATH):
            print("Transcript not found. Run your recorder first.")
            return
        with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
            transcript_text = f.read().strip()

    if not transcript_text:
        print("Transcript is empty.")
        return

    print(f"\n Transcript length: {len(transcript_text)} characters")

    # --- Summarize in chunks if large ---
    max_chunk_size = 2500
    chunks = [transcript_text[i:i + max_chunk_size] for i in range(0, len(transcript_text), max_chunk_size)]
    summaries = []

    for idx, chunk in enumerate(chunks, 1):
        print(f"\n🔍 Summarizing chunk {idx}/{len(chunks)}...")
        prompt_summary = f"""
You are an intelligent AI summarizer. Summarize the following text clearly and concisely.

Text:
{chunk}

Return only a concise summary. End your answer with: [END]
"""
        summary_chunk = run_llm(prompt_summary)
        summaries.append(summary_chunk)

    final_summary = "\n".join(summaries)

    # --- Generate suggestions ---
    prompt_suggestions = f"""
Analyze the following user transcript and provide 3 short, actionable suggestions
to improve productivity or focus.

Text:
{transcript_text}

Return only bullet points using '-' (no * or **). End with [END].
"""
    suggestions = run_llm(prompt_suggestions)

    # --- Save outputs ---
    os.makedirs("output", exist_ok=True)
    try:
        with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
            f.write(final_summary)
        with open(SUGGESTIONS_PATH, "w", encoding="utf-8") as f:
            f.write(suggestions)
    except Exception as e:
        print("Error saving files:", e)
        return

    print("\n Summary and suggestions saved to 'output/' folder.")
    print("\n--- Summary ---\n", final_summary)
    print("\n--- Suggestions ---\n", suggestions)

    return SUMMARY_PATH


if __name__ == "__main__":
    summarize_session()
