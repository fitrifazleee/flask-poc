from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
click_logs = []

@app.route('/')
def home():
    return render_template('index.html', logs=click_logs)

@app.route('/click', methods=['POST'])
def click():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    click_logs.append(timestamp)
    return jsonify({"status": "success", "time": timestamp})

if __name__ == '__main__':
    app.run()
