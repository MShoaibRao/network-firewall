# from flask import Flask
# from flask_pymongo import PyMongo
# from scapy.all import sniff
# import subprocess
# import re
# import speedtest
# import ipaddress
# import time

# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/IntelliFirewall"
# mongo = PyMongo(app)
# db = mongo.db
# collection = db['dasboard_items']

# # List of CIDRs for each app
# app_cidrs = {
#     "Google": ["8.8.8.0/24", "8.8.4.0/24", "172.217.0.0/16", "142.250.0.0/16"],
#     "Facebook": ["69.63.176.0/20", "69.171.224.0/19", "157.240.0.0/16"],
#     "TikTok": ["47.88.0.0/16", "47.89.0.0/16"],
#     "YouTube": ["172.217.0.0/16", "173.194.0.0/16"],
#     "VPN": ["1.0.0.0/8"]
# }

# def get_connected_devices():
#     arp_output = subprocess.check_output("arp -a", shell=True, text=True)
#     devices_count = re.findall(r'\d+', arp_output)
#     return int(devices_count[0]) if devices_count else 0

# def measure_internet_speed():
#     st = speedtest.Speedtest()
#     st.get_best_server()
#     download_speed = st.download() / 10**6  # Convert to Mbps
#     upload_speed = st.upload() / 10**6  # Convert to Mbps
#     return download_speed, upload_speed

# def calculate_vpn_traffic(packet):
#     vpn_traffic = sum(len(packet) for cidrs in app_cidrs.values() for cidr in cidrs if ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr))
#     return vpn_traffic

# def calculate_unknown_traffic(packet):
#     unknown_traffic = len(packet) if not any(ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr) for cidrs in app_cidrs.values() for cidr in cidrs) else 0
#     #unknown_traffic = len(packet) if not any(ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr) for cidrs in app_cidrs.values() for cidr in cidrs)
#     return unknown_traffic

# def update_dashboard():
#     connected_devices = get_connected_devices()
#     download_speed, upload_speed = measure_internet_speed()
#     sniffed_packets = sniff(timeout=10, iface="wlp0s20f3", prn=lambda packet: packet)
#     vpn_traffic = sum(calculate_vpn_traffic(packet) for packet in sniffed_packets)
#     unknown_traffic = sum(calculate_unknown_traffic(packet) for packet in sniffed_packets)
    
#     # Add all data as a single row in the collection
#     collection.insertz_one({
#         "Connected_Devices": connected_devices,
#         "Net_Speed": {"Download": download_speed, "Upload": upload_speed},
#         "VPN_Traffic": vpn_traffic,
#         "Unknown_Traffic": unknown_traffic
#     })

# @app.route('/')
# def index():
#     return "IntelliFirewall is up and running!"

# if __name__ == "__main__":
#     while True:
#         update_dashboard()
#         time.sleep(10)




# ////////////////////////////////////////////////////


from flask import Flask
from flask_pymongo import PyMongo
from scapy.all import sniff
import subprocess
import re
import speedtest
import ipaddress
import time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/IntelliFirewall"
mongo = PyMongo(app)
db = mongo.db
collection = db['dasboard_items']

# List of CIDRs for each app
app_cidrs = {
    "Google": ["8.8.8.0/24", "8.8.4.0/24", "172.217.0.0/16", "142.250.0.0/16"],
    "Facebook": ["69.63.176.0/20", "69.171.224.0/19", "157.240.0.0/16"],
    "TikTok": ["47.88.0.0/16", "47.89.0.0/16"],
    "YouTube": ["172.217.0.0/16", "173.194.0.0/16"],
    "VPN": ["1.0.0.0/8"]
}





def calculate_vpn_traffic(packet):
    if 'IP' in packet:
        vpn_traffic = sum(len(packet) for cidrs in app_cidrs.values() for cidr in cidrs if ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr))
        return vpn_traffic

def calculate_unknown_traffic(packet):
    if 'IP' in packet:
        unknown_traffic = len(packet) if not any(ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr) for cidrs in app_cidrs.values() for cidr in cidrs) else 0
        return unknown_traffic

def update_dashboard():
    sniffed_packets = sniff(timeout=10, iface="wlp0s20f3", prn=lambda packet: packet)
    vpn_traffic = sum(calculate_vpn_traffic(packet) for packet in sniffed_packets)
    unknown_traffic = sum(calculate_unknown_traffic(packet) for packet in sniffed_packets)
    
    # Add all data as a single row in the collection
    collection.insert_one({
        # "Connected_Devices": connected_devices,
        # "Net_Speed": {"Download": download_speed, "Upload": upload_speed},
        "VPN_Traffic": vpn_traffic,
        "Unknown_Traffic": unknown_traffic
    })

@app.route('/')
def index():
    return "IntelliFirewall is up and running!"

if __name__ == "__main__":
    while True:
        update_dashboard()
        time.sleep(10)
