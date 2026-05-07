import pyautogui
import time
import os
import subprocess

# Setup Paths and Target URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BTN_IMAGE = os.path.join(BASE_DIR, 'button_target.png')
DROP_IMAGE = os.path.join(BASE_DIR, 'dropdown_target.png')
TARGET_URL = "https://flask-i9lyr06rw-fitrifazleee-7841s-projects.vercel.app/click"
def launch_browser():
    print(f"[{time.strftime('%H:%M:%S')}] Browser missing or closed. Launching Chromium...")
    
    # DEVNULL acts as a black hole to swallow all those annoying Chromium DEPRECATED_ENDPOINT errors
    subprocess.Popen(
        ['chromium-browser', '--kiosk', TARGET_URL],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print("Waiting 10 seconds for Vercel to fully load...")
    time.sleep(10)

def search_and_click(image_path, description):
    print(f"Scanning screen for: {description}...")
    
    for attempt in range(3):
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                print(f"-> Target locked at {location}! Executing click.")
                pyautogui.moveTo(location.x, location.y, duration=0.75, tween=pyautogui.easeInOutQuad)
                pyautogui.click()
                return True
        except Exception as e:
            # We now print the EXACT error so we know if a library is missing!
            print(f"-> Vision Engine Error on attempt {attempt+1}: {e}")
            
        time.sleep(2) 
        
    print(f"-> FAILED: Could not find {description}.")
    return False

def run_automation_flow():
    print("--- AUTOMATION SEQUENCE INITIATED ---")
    
    if not search_and_click(BTN_IMAGE, "Green 'Tekan Saya' Button"):
        launch_browser()
        
        if not search_and_click(BTN_IMAGE, "Green 'Tekan Saya' Button (Post-Launch)"):
            print("CRITICAL ERROR: Cannot find UI even after launching browser. Aborting.")
            return

    print("Main button clicked. Waiting for dropdown UI to render...")
    time.sleep(1.5)

    if search_and_click(DROP_IMAGE, "'Log Time' Option"):
        print("--- AUTOMATION SEQUENCE SUCCESSFUL ---")
    else:
        print("ERROR: Dropdown did not appear or target was obscured.")

if __name__ == "__main__":
    run_automation_flow()
