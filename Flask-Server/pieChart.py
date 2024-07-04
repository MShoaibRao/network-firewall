from flask import Flask
from flask_pymongo import PyMongo
from scapy.all import sniff
import ipaddress
import subprocess
import re
from datetime import datetime
import time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/IntelliFirewall"
mongo = PyMongo(app)
db = mongo.db
collection = db['pie_charts']
collectionDash = db['dasboard_items']
line_chart_collection = db['line_charts']

# List of CIDRs for each app
app_cidrs = {
    "Google": ["8.8.8.0/24", "8.8.4.0/24", "172.217.0.0/16", "142.250.0.0/16", "142.251.0.0/16"],
    "Facebook": ["69.63.176.0/20", "69.171.224.0/19", "157.240.0.0/16"],
    "TikTok": ["47.88.0.0/16", "47.89.0.0/16"],
    "ISP": ["119.160.0.0/16", "47.254.145.0/24"]
}


def calculate_traffic(packet):
    if 'IP' in packet and packet.sniffed_on == "wlp0s20f3":  # Check if packet is from the specified interface
        for app, cidrs in app_cidrs.items():
            app_traffic = 0
            for cidr in cidrs:
                try:
                    if ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr):  # Convert to IPv4Address object
                        app_traffic += len(packet)
                except ValueError:
                    print(f"Error: {cidr} is not a valid IPv4 CIDR block.")
            if app_traffic > 0:
                collection.update_one(
                    {'id': app},  # Use 'id' as the field name for the app ID
                    {'$inc': {'value': app_traffic}, '$set': {'label': app.upper()}},
                    upsert=True
                )
        # Handle unknown packets separately
        if not any(ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr) for cidrs in app_cidrs.values() for cidr in cidrs):
            collection.update_one(
                {'id': 'Unknown'},  # Use 'id' as the field name for the UnknownTraffic ID
                {'$inc': {'value': len(packet)}, '$set': {'label': 'UNKNOWN'}},
                upsert=True
            )

        collectionDash.update_one(
        {},
        {'$set': {'Unknown_traffic': (len(packet))/1024}},
        upsert=True
    )
        





@app.route('/')
def index():
    return "IntelliFirewall is up and running!"

if __name__ == "__main__":
    while True:
        sniff(prn=calculate_traffic, store=0, iface="wlp0s20f3")
        time.sleep(1)
