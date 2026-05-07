
# Surfactor Solar Dashboard: Hybrid Edge-to-Cloud Implementation Guide

## 1. Core Architecture & Hardware Stack
This phase replaces the unreliable Huidu player with a thermally managed edge controller.

**Hardware Required:**
*   **Edge Controller:** Raspberry Pi CM5.
*   **Carrier Board:** A Waveshare base board (ideal for serving as a Kiosk display) to provide the necessary HDMI out, Ethernet, and USB ports.
*   **Thermal Management:** An active cooling solution (e.g., Ice Tower cooler or a dedicated Noctua 5V fan). Passive cooling will fail in a $70^\circ\text{C}$ metal box.
*   **Display Interface:** Standard HDMI cable connecting the Waveshare board directly to the LED Sending Box.

**Software Stack:**
*   **OS:** Raspberry Pi OS (Bookworm, 64-bit with Desktop environment).
*   **Local Display:** Chromium Browser (launched via terminal in `--kiosk` mode).
*   **Data Pipeline:** Python 3.11 (utilizing `requests` and `schedule` libraries).
*   **Cloud Hosting:** Vercel (for the remote dashboard replica).

---

## 2. Step-by-Step Implementation Workflow

### Phase A: Local Edge Setup (The Kiosk)
First, we ensure the CM5 boots directly into a fullscreen, lock-down browser displaying the solar data.

1.  **Flash the OS:** Install Raspberry Pi OS on the CM5.
2.  **Configure Auto-Login:** Set the Pi to automatically log into the desktop environment upon power-up.
3.  **Create the Kiosk Autostart Script:**
    We need Chromium to launch immediately and hide the mouse cursor.
    *   Open terminal: `nano ~/.config/wayfire.ini` (or the autostart file for your specific display server).
    *   Add the launch command: 
        `chromium-browser --kiosk --noerrdialogs --disable-infobars --check-for-update-interval=31536000 http://localhost:5000`

### Phase B: The Data Pipeline (Python Bridge)
This script sits on the CM5. It constantly asks the NUC PLC for the latest solar data, updates the local display, and mirrors that data to your Vercel cloud app.

1.  **Setup the Virtual Environment:**
    ```bash
    mkdir solar_bridge && cd solar_bridge
    python -m venv venv
    source venv/bin/activate
    pip install requests schedule flask
    ```

2.  **Write the Hybrid Bridge Script (`bridge.py`):**
    ```python
    import requests
    import time
    from datetime import datetime

    NUC_URL = "http://<NUC_IP_ADDRESS>/api/solar_data"
    VERCEL_URL = "https://your-vercel-app.vercel.app/update"

    def fetch_and_sync():
        try:
            # 1. Pull data from the NUC
            nuc_response = requests.get(NUC_URL, timeout=5)
            nuc_response.raise_for_status()
            solar_data = nuc_response.json()
            
            print(f"Data fetched locally at {datetime.now()}")

            # 2. Update local Flask dashboard (Optional: write to a local JSON file that your HTML reads)
            # update_local_dashboard(solar_data)

            # 3. Push to Vercel (Cloud Sync)
            cloud_response = requests.post(VERCEL_URL, json=solar_data, timeout=5)
            if cloud_response.status_code == 200:
                print("Cloud sync successful.")
                
        except requests.exceptions.RequestException as e:
            # Accurately log the specific hardware communication issue
            print(f"Unsuccessful data polling from NUC or Vercel: {e}")

    # Run the sync every 10 seconds
    while True:
        fetch_and_sync()
        time.sleep(10)
    ```

### Phase C: Cloud Dashboard Deployment (Vercel)
You will replicate the exact workflow from your recent PoC.
1.  Create a Flask app with a clean HTML/CSS template designed for the Surfactor layout.
2.  Create an endpoint (e.g., `@app.route('/update', methods=['POST'])`) that accepts the JSON payload from your CM5.
3.  Push to GitHub and let Vercel deploy the live link.

---

## 3. Resilience: The Hardware Watchdog
Industrial environments experience power dips and network drops. The system must heal itself without human intervention.

**Implement a Cronjob Reboot:**
If the script crashes or the Wi-Fi drops, the Pi needs to know.
1.  Open the crontab: `crontab -e`
2.  Add a rule to reboot the machine daily at 3:00 AM to clear out any memory leaks or cached data:
    `0 3 * * * /sbin/shutdown -r now`
3.  Set your `bridge.py` script to run automatically on boot using a systemd service file.

---

## 4. Early Awareness: Potential Issues & Limitations

As you move from the lab to the Johor Bahru guardhouse, prepare for these specific challenges:

*   **Computational Overload:** The CM5 is powerful, but it has limits. Ensure the CM5 is *only* dedicated to fetching data and rendering the local dashboard. Do not run local cloud flows for voice generation or heavy AI models simultaneously on this specific Pi, because it slows down the controller and will cause the screen to stutter or hang. Keep this pipeline ruthlessly lean.
*   **Unsuccessful Data Polling (Network Timeouts):** The local network between the NUC PLC and the CM5 might drop packets due to electromagnetic interference (EMI) from nearby heavy machinery. Ensure your Python script includes `timeout=5` (as shown above) and `try/except` blocks. If the code doesn't handle a timeout gracefully, the entire script will crash on the first missed ping.
*   **Thermal Throttling:** Even with active cooling, monitor the Pi's internal temperature during the first week. You can add a line in your Python script to read `/sys/class/thermal/thermal_zone0/temp` and push that data to Vercel. If it consistently exceeds $80^\circ\text{C}$, you will need to physically relocate the enclosure. 
*   **SD Card Corruption:** Constantly writing logs to an SD card will destroy it within months. Modify your local scripts to log errors to RAM (tmpfs) or exclusively push logs to the Vercel cloud to extend the life of the edge hardware.
```
