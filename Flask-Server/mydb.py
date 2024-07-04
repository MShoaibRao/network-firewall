from flask import Flask
from flask_pymongo import PyMongo
import subprocess
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/IntelliFirewall"
db = PyMongo(app).db

current_connected_devices = {}

# Function to fetch currently connected devices
def fetch_connected_devices():
    command = "arp -a"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        print(f"Error fetching connected devices: {error}")
        return None

    return parse_device_output(output.decode())

# Function to parse the command output
def parse_device_output(output):
    devices = []
    lines = output.split("\n")

    for line in lines:
        if line.strip():
            parts = line.split()
            ip = parts[1].strip("()")
            mac = parts[3]
            devices.append({"ip": ip, "mac": mac})

    return devices

# Function to update the database
def update_database():
    global current_connected_devices
    devices = fetch_connected_devices()

    if devices is None:
        return
    
    # Convert devices list to dictionary by mac
    current_devices = {device["mac"]: device for device in devices}

    # Check for new connections and disconnections
    new_connections = set(current_devices) - set(current_connected_devices)
    disconnections = set(current_connected_devices) - set(current_devices)

    # Update the database with connection and disconnection events
    for mac in new_connections:
        device = current_devices[mac]
        device["connect_time"] = datetime.datetime.now()
        device["status"] = "connected"
        db.divice_reports.insert_one(device)
        print(f"Device connected: {device}")

    for mac in disconnections:
        device = current_connected_devices[mac]
        disconnect_time = datetime.datetime.now()
        
        # Calculate duration
        connect_time = device.get("connect_time")
        duration = (disconnect_time - connect_time).total_seconds() if connect_time else None
        
        # Update the record with disconnect time and duration
        db.divice_reports.update_one(
            {"mac": mac, "status": "connected"},
            {"$set": {
                "status": "disconnected",
                "disconnect_time": disconnect_time,
                "duration": duration
            }}
        )
        print(f"Device disconnected: {device}")

    # Update the current connected devices dictionary
    current_connected_devices = current_devices

# Schedule the function to run every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(update_database, 'interval', seconds=10)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
