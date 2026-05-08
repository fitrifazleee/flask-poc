import pyautogui
import time
import os
import subprocess

# Setup Paths and Target URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BTN_IMAGE = os.path.join(BASE_DIR, 'button_target.png')
DROP_IMAGE = os.path.join(BASE_DIR, 'dropdown_target.png')

# CHANGED: Now using your permanent production URL!
TARGET_URL = "https://flask-poc.vercel.app" 

def launch_browser():
    print(f"[{time.strftime('%H:%M:%S')}] Browser missing or closed. Launching Chromium...")
    
    # DEVNULL acts as a black hole to swallow all annoying Chromium background errors
    subprocess.Popen(
        ['chromium-browser', '--kiosk', TARGET_URL],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    print("Waiting 10 seconds for Vercel to fully load...")
    time.sleep(10)

def search_and_click(image_path, description):
    print(f"Scanning screen for: {description}...")
    
    # Give the vision engine 5 attempts (6 seconds total) to find the target
    for attempt in range(5):
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                print(f"-> Target locked at {location}! Executing click.")
                pyautogui.moveTo(location.x, location.y, duration=0.8, tween=pyautogui.easeInOutQuad)
                pyautogui.click()
                return True
        except Exception as e:
            # Prints exact errors (like missing numpy) instead of failing silently
            print(f"-> Vision Engine Error on attempt {attempt+1}: {e}")
            
        time.sleep(2) 
        
    print(f"-> FAILED: Could not find {description}.")
    return False

def run_automation_flow():
    print("--- AUTOMATION SEQUENCE INITIATED ---")
    
    # STEP 1: Find the Green Button
    if not search_and_click(BTN_IMAGE, "Green 'Tekan Saya' Button"):
        # Self-healing: If it fails, launch the browser
        launch_browser()
        
        # Try finding the main button one more time
        if not search_and_click(BTN_IMAGE, "Green 'Tekan Saya' Button (Post-Launch)"):
            print("CRITICAL ERROR: Cannot find UI even after launching browser. Aborting.")
            return

    # STEP 2: Wait for HTML to render the Dropdown
    print("Main button clicked. Waiting for dropdown UI to render...")
    time.sleep(2)

    # STEP 3: Find the Correct Dropdown Option
    if search_and_click(DROP_IMAGE, "'Log Time' Option"):
        print("--- AUTOMATION SEQUENCE SUCCESSFUL ---")
    else:
        print("ERROR: Dropdown did not appear or target was obscured.")

if __name__ == "__main__":
    run_automation_flow()
