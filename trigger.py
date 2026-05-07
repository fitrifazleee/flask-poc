import requests

# Updated to use your permanent URL AND the correct backend endpoint
URL = "https://flask-poc.vercel.app/click"

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
