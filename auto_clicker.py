import pyautogui
import time
import os
import subprocess

# Setup Paths and Target URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BTN_IMAGE = os.path.join(BASE_DIR, 'button_target.png')
DROP_IMAGE = os.path.join(BASE_DIR, 'dropdown_target.png')
TARGET_URL = "https://flask-a48pwj0r6-fitrifazleee-7841s-projects.vercel.app" # Ensure this is your actual URL

def launch_browser():
    print(f"[{time.strftime('%H:%M:%S')}] Browser missing or closed. Launching Chromium...")
    # This command talks directly to the Linux OS to open the browser in Kiosk mode
    subprocess.Popen(['chromium-browser', '--kiosk', TARGET_URL])
    
    print("Waiting 10 seconds for Vercel to fully load...")
    time.sleep(10)

def search_and_click(image_path, description):
    print(f"Scanning screen for: {description}...")
    
    # We give it 3 attempts (6 seconds) to find the image before giving up
    for attempt in range(3):
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                print(f"-> Target locked at {location}! Executing click.")
                pyautogui.moveTo(location.x, location.y, duration=0.8, tween=pyautogui.easeInOutQuad)
                pyautogui.click()
                return True
        except Exception as e:
            pass # Ignore minor vision errors and keep trying
            
        time.sleep(2) # Wait 2 seconds before checking the screen again
        
    print(f"-> FAILED: Could not find {description}.")
    return False

def run_automation_flow():
    print("--- AUTOMATION SEQUENCE INITIATED ---")
    
    # STEP 1: Look for the Main Button
    if not search_and_click(BTN_IMAGE, "Green 'Tekan Saya' Button"):
        # If it fails, trigger the self-healing protocol (open browser)
        launch_browser()
        
        # Try finding the main button one more time after launching
        if not search_and_click(BTN_IMAGE, "Green 'Tekan Saya' Button (Post-Launch)"):
            print("CRITICAL ERROR: Cannot find UI even after launching browser. Aborting.")
            return

    # STEP 2: Main button was clicked. Wait for the HTML dropdown animation.
    print("Main button clicked. Waiting for dropdown UI to render...")
    time.sleep(1.5)

    # STEP 3: Look for the specific true dropdown option among the dummies
    if search_and_click(DROP_IMAGE, "Yellow 'Log Time' Option"):
        print("--- AUTOMATION SEQUENCE SUCCESSFUL ---")
    else:
        print("ERROR: Dropdown did not appear or target was obscured.")

if __name__ == "__main__":
    run_automation_flow() 
