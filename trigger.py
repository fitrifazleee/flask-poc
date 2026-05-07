import requests

# This is the URL you just got from Vercel
URL = "https://flask-a48pwj0r6-fitrifazleee-7841s-projects.vercel.app"
print("Sending 'Button Press' signal to the cloud...")

try:
    # This simulates a sensor or physical button event
    response = requests.post(URL)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Cloud logged the time as: {data['time']}")
    else:
        print(f"Failed. Server returned: {response.status_code}")
except Exception as e:
    print(f"Error connecting to cloud: {e}")
