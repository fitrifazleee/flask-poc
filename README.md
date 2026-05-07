# IIoT PoC: Edge-to-Cloud Event Logger

## Overview
This repository contains a Proof of Concept (PoC) demonstrating a foundational Industrial Internet of Things (IIoT) architecture. It bridges an edge device with a serverless cloud dashboard. The project utilizes a Raspberry Pi CM5 as the edge controller, which triggers HTTP requests to a Python Flask application deployed on Vercel's serverless infrastructure.

## Technology Stack
*   **Edge Hardware:** Raspberry Pi CM5
*   **Backend Framework:** Python 3.11.2, Flask
*   **Frontend:** HTML, JavaScript (Fetch API)
*   **Version Control:** Git, GitHub
*   **Cloud Hosting:** Vercel (Serverless Functions)

---

## Implementation Flow

### Phase 1: Environment Setup & Core Files
To maintain system stability on the Raspberry Pi, a Python Virtual Environment (`venv`) was utilized. 

**Directory Structure:**
```text
flask_poc/
├── venv/                 # Python virtual environment (ignored in Git)
├── templates/
│   └── index.html        # Frontend dashboard
├── app.py                # Flask backend logic
├── requirements.txt      # Dependency list
├── vercel.json           # Vercel deployment configuration
├── .gitignore            # Excluded files
└── trigger.py            # Edge simulation script
```

**1. `requirements.txt`**
```text
Flask==3.0.3
requests==2.31.0
```

**2. `vercel.json`**
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/app.py"
    }
  ]
}
```

**3. `app.py`** (Includes GMT+8 Timezone adjustment)
```python
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
click_logs = []

@app.route('/')
def home():
    return render_template('index.html', logs=click_logs)

@app.route('/click', methods=['POST'])
def click():
    # Set timezone to GMT+8
    malaysia_tz = timezone(timedelta(hours=8))
    timestamp = datetime.now(malaysia_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    click_logs.append(timestamp)
    return jsonify({"status": "success", "time": timestamp})

if __name__ == '__main__':
    app.run()
```

**4. `templates/index.html`**
```html
<!DOCTYPE html>
<html>
<body>
    <button id="clickBtn">Tekan Saya</button>
    <p>Total Clicks: {{ logs|length }}</p>
    <ul>
        {% for log in logs %}
        <li>{{ log }}</li>
        {% endfor %}
    </ul>
    <script>
        document.getElementById('clickBtn').addEventListener('click', function() {
            fetch('/click', { method: 'POST' })
            .then(response => location.reload());
        });
    </script>
</body>
</html>
```

### Phase 2: Version Control (GitHub)
The local codebase was pushed to a GitHub repository to act as the pipeline for Vercel. Standard Git tracking was used, overriding password prompts with a GitHub Personal Access Token (PAT).

```bash
git init
git add .
git commit -m "Initial PoC commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Phase 3: Cloud Deployment (Vercel)
The GitHub repository was imported directly into the Vercel Dashboard. Vercel automatically detected the Python framework via the `vercel.json` file, built the environment based on `requirements.txt`, and generated a live public URL. CI/CD was established: any subsequent `git push` to the `main` branch automatically triggers a new deployment.

### Phase 4: Edge Device Trigger Simulation
To simulate an industrial sensor or automated process pushing data to the cloud, a separate script was run locally on the Raspberry Pi terminal.

**`trigger.py`**
```python
import requests

# Live Vercel URL
URL = "https://your-live-url.vercel.app/click"

try:
    response = requests.post(URL)
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Cloud logged the time as: {data['time']}")
except Exception as e:
    print(f"Connection error: {e}")
```

---

## Troubleshooting & Lessons Learned

During the execution of this PoC, three major issues were encountered and resolved. These serve as critical lessons for edge-to-cloud deployments.

### Issue 1: Vercel Bundle Size Limitation (The `venv` Trap)
*   **The Error:** `Total bundle size (851.27 MB) exceeds Lambda ephemeral storage limit (500 MB).`
*   **The Cause:** Running `git add .` on the Raspberry Pi blindly tracked the entire `venv` directory (containing the full Python operating system) as well as hidden Linux cache folders (like Chromium's `.config`). Vercel attempted to upload this massive file structure to a serverless function, which has strict size limits.
*   **The Solution:** Purged Git's cache of the heavy folders and created a `.gitignore` file to ensure only lightweight application files were tracked.
    ```bash
    git rm -r --cached .
    # Created .gitignore with "venv/" and "__pycache__/"
    git add app.py requirements.txt vercel.json .gitignore templates/
    git commit -m "Emergency cleanup"
    git push origin main
    ```

### Issue 2: Vercel Edge Network Routing (404 Error)
*   **The Error:** Vercel returned a `404: NOT_FOUND` screen despite a successful build.
*   **The Cause:** Vercel's Edge Network recently updated how it handles serverless function routing. The initial `vercel.json` used the legacy `"routes"` keyword, which caused Vercel's router to fail to connect the incoming web traffic to the `app.py` script.
*   **The Solution:** Updated `vercel.json` to use the modern `"rewrites"` syntax.
    ```json
    "rewrites": [
      {
        "source": "/(.*)",
        "destination": "/app.py"
      }
    ]
    ```

### Issue 3: Git Synchronization and Divergent Branches
*   **The Error:** `fatal: refusing to merge unrelated histories` and `Updates were rejected because the remote contains work that you do not have locally.`
*   **The Cause:** As changes were made (like adding the Vercel routing fix), the local Raspberry Pi and the remote GitHub repository fell out of sync. Furthermore, attempting to merge them triggered a safeguard because the initial initialization created divergent, unrelated Git timelines.
*   **The Solution:** Forced the timelines to merge by allowing unrelated histories, then pulling the remote changes before pushing the new updates.
    ```bash
    git config pull.rebase false
    git pull origin main --allow-unrelated-histories
    git push origin main
    ```
```
