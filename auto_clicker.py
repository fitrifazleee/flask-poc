import pyautogui
import time 
import os

#finding image file correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, 'button_target.png')

def find_and_click():
	print(f"[{time.strftime('%H:%M:%S')}] Scanning for button...")

