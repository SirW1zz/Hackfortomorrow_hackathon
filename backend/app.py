from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from backend.camera import scan_class
from backend.database import clean_database_names
import random
import time
import datetime
import atexit

# Clean DB on startup
clean_database_names()

app = Flask(__name__)

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Global to store scheduled jobs and last scan result
scheduled_jobs = []
last_scan_result = {"timestamp": None, "detected": [], "type": None}

def perform_scan(reason="Scheduled"):
    global last_scan_result
    print(f"[{datetime.datetime.now()}] Starting {reason} Scan...")
    detected = scan_class(duration=15)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {reason} Scan Complete. Detected: {detected}")
    
    last_scan_result = {
        "timestamp": timestamp,
        "detected": detected,
        "type": reason
    }
    return detected

def schedule_random_scans(start_hour, end_hour):
    """
    Schedules random scans between start and end hours.
    This is a simplified version: it just adds a random job in the next hour.
    In a real app, you'd have more complex logic.
    """
    # For this hackathon, let's just add a recurring job that runs every 30 mins with some jitter
    # Or better, just a fixed interval of 30 mins as requested "random, timed... like 15 -30 - 45 mins"
    pass

# Add a background job that runs every 30 minutes to simulate "random" checks
# We add jitter to make it slightly random
scheduler.add_job(
    func=perform_scan,
    args=["Random"],
    trigger="interval",
    minutes=30,
    jitter=300, # +/- 5 minutes
    id="random_scan",
    replace_existing=True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set-schedule', methods=['POST'])
def set_schedule():
    data = request.json
    times = data.get('times', [])
    
    # Clear existing scheduled time jobs
    for job in scheduled_jobs:
        try:
            scheduler.remove_job(job)
        except:
            pass
    scheduled_jobs.clear()
    
    # Add new jobs
    for t in times:
        hour, minute = map(int, t.split(':'))
        job = scheduler.add_job(
            func=perform_scan,
            args=["Fixed Time"],
            trigger='cron',
            hour=hour,
            minute=minute
        )
        scheduled_jobs.append(job.id)
        
    return jsonify({"message": f"Scheduled {len(times)} scans."})

@app.route('/scan-now', methods=['POST'])
def scan_now():
    detected = perform_scan(reason="Manual")
    return jsonify({"status": "success", "detected": detected})

@app.route('/last-scan')
def get_last_scan():
    return jsonify(last_scan_result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
