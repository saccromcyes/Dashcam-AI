import pytesseract
from PIL import Image
import os
import json
from datetime import datetime
from capture.user_logger import log_event

# Manual Tesseract path (use if not added to PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_images(screenshot_paths):
    """
    Takes a list of image paths (or a single path), extracts text from each using Tesseract OCR,
    logs it, and returns a structured list.
    """
    results = []
    try:
        if isinstance(screenshot_paths, str):
            screenshot_paths = [screenshot_paths]  # Handle single file input

        for image_path in screenshot_paths:
            if not os.path.exists(image_path):
                print(f"[ocr] Skipping missing file: {image_path}")
                continue

            img = Image.open(image_path)
            text = pytesseract.image_to_string(img).strip()

            result = {
                "timestamp": datetime.now().isoformat(),
                "image_path": image_path,
                "extracted_text": text
            }

            print(f"[ocr] Processed {os.path.basename(image_path)}")
            results.append(result)

            # Log each OCR text
            log_event("ocr_text", text if text else "No text detected")

        # Save OCR results
        log_path = os.path.join("data", "logs", "ocr_log.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        print(f"[ocr] OCR completed. Results saved to {log_path}")
        return results

    except Exception as e:
        print(f"[ocr] Error during OCR: {e}")
        return []
