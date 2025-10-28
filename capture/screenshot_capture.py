import pyautogui
import os
import time
from datetime import datetime

def capture_screenshots(interval=5, count=5):
    """
    Captures periodic screenshots and saves them to data/screenshots/.
    :param interval: Time gap between screenshots (in seconds)
    :param count: Number of screenshots to take
    :return: List of saved screenshot file paths
    """
    os.makedirs("data/screenshots", exist_ok=True)
    print("[screen] capturing screenshots...")

    screenshot_paths = []  # store all file paths

    for i in range(count):
        filename = datetime.now().strftime("data/screenshots/%Y-%m-%d_%H-%M-%S.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        screenshot_paths.append(filename)
        print(f"[screen] saved {filename}")
        time.sleep(interval)

    print(f"[screen] capture complete. Total: {len(screenshot_paths)} screenshots.")
    return screenshot_paths  # returning list

if __name__ == "__main__":
    paths = capture_screenshots()
    print("Captured files:", paths)


