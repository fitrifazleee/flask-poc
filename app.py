from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
click_logs = []

@app.route('/')
def home():
    return render_template('index.html', logs=click_logs)

@app.route('/click', methods=['POST'])
def click():
    # Create a timezone object for Malaysia (UTC + 8 hours)
    malaysia_tz = timezone(timedelta(hours=8))
    
    # Get current time and apply the timezone
    timestamp = datetime.now(malaysia_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    click_logs.append(timestamp)
    return jsonify({"status": "success", "time": timestamp})

if __name__ == '__main__':
    app.run()
