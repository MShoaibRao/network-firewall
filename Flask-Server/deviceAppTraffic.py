from flask import Flask
from flask_pymongo import PyMongo
from scapy.all import sniff
import ipaddress  # Add this import
import subprocess
import re
import time

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/IntelliFirewall"
mongo = PyMongo(app)
db = mongo.db
collection = db['bar_charts']

# List of CIDRs for each app
app_cidrs = {
    "Google": ["8.8.8.0/24", "8.8.4.0/24", "172.217.0.0/16", "142.250.0.0/16", "142.251.0.0/16"],
    "Facebook": ["69.63.176.0/20", "69.171.224.0/19", "157.240.0.0/16"],
    "local": ["119.160.0.0/16", "47.89.0.0/16"],
    "YouTube": ["172.217.0.0/16", "173.194.0.0/16", "2.16.241.0/24", "142.251.0.0/16"]
}

def get_device_macs():
    arp_output = subprocess.check_output("arp -a", shell=True, text=True)
    device_macs = re.findall(r'(?:[0-9a-fA-F]:?){12}', arp_output)
    return device_macs

def calculate_traffic(packet):
    if 'IP' in packet:
        device_mac = packet['Ethernet'].src  # Assuming MAC address is in Ethernet layer
        device_macs = get_device_macs()
        if device_mac in device_macs:
            # app_traffic = 1
            
            for app, cidrs in app_cidrs.items():
                app_traffic = 0
                for cidr in cidrs:
                    if ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr):  # Convert to IPv4Address object
                        app_traffic += len(packet)
                # if app_traffic > 0:
                # app_traffic_mb = app_traffic / (1024 * 1024)
                # print(f"Device MAC: {device_mac}, App: {app}, Traffic: {app_traffic_mb} bytes")
                # collection.update_one({'DeviceMAC': device_mac}, {'$inc': {f'{app}_kbs': app_traffic_mb}}, upsert=True)
                # if app_traffic < 0.1:
                    # collection.update_one({'DeviceMAC': device_mac}, {'$inc': {f'{app}_kbs': 0.1/ (1024 * 1024)}}, upsert=True)
                collection.update_one({'DeviceMAC': device_mac}, {'$inc': {f'{app}_kbs': app_traffic/ (1024 * 1024)}}, upsert=True)

        else:
            print(f"Packet source MAC {device_mac} is not a recognized device MAC.")


@app.route('/')
def index():
    return "IntelliFirewall is up and running!"

if __name__ == "__main__":
    while True:
        device_macs = get_device_macs()
        print("Device MACs:", device_macs)
        sniff(prn=calculate_traffic, store=0, iface="wlp0s20f3")
        time.sleep(10)



# ///////////////////////////////////////


# from flask import Flask
# from flask_pymongo import PyMongo
# from scapy.all import sniff
# import ipaddress
# import subprocess
# import re
# import time

# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/IntelliFirewall"
# mongo = PyMongo(app)
# db = mongo.db
# collection = db['bar_charts']

# # List of CIDRs for each app
# app_cidrs = {
#     "Google": ["8.8.8.0/24", "8.8.4.0/24", "172.217.0.0/16", "142.250.0.0/16", "119.160.0.0/16"],
#     "Facebook": ["69.63.176.0/20", "69.171.224.0/19", "157.240.0.0/16"],
#     "TikTok": ["47.88.0.0/16", "47.89.0.0/16"],
#     "YouTube": ["172.217.0.0/16", "173.194.0.0/16"]
# }

# def get_device_macs():
#     arp_output = subprocess.check_output("arp -a", shell=True, text=True)
#     device_macs = re.findall(r'(?:[0-9a-fA-F]:?){12}', arp_output)
#     return device_macs

# def update_device_traffic(device_mac, app_traffic_default):
#     collection.update_one({'DeviceMAC': device_mac}, {'$set': app_traffic_default}, upsert=True)


# def calculate_traffic(packet):
#     if 'IP' in packet:
#         device_mac = packet['Ethernet'].src  # Assuming MAC address is in Ethernet layer
#         if device_mac == "8c:f8:c5:c0:8e:74":  # Ignore this MAC address
#             return
#         device_macs = get_device_macs()
#         if device_mac in device_macs:
#             for app, cidrs in app_cidrs.items():
#                 app_traffic = 0  # Start with default value of 0
#                 for cidr in cidrs:
#                     if ipaddress.ip_address(packet['IP'].dst) in ipaddress.ip_network(cidr):
#                         app_traffic += len(packet)
#                 app_traffic_default = {f'{app}_kbs': app_traffic}
#                 app_traffic_mb = app_traffic / (1024 * 1024)
#                 print(f"Device MAC: {device_mac}, App: {app}, Traffic: {app_traffic} bytes")
#                 collection.update_one({'DeviceMAC': device_mac}, {'$inc': app_traffic_default}, upsert=True)
#         else:
#             print(f"Packet source MAC {device_mac} is not a recognized device MAC.")
#             app_traffic_default = {f'{app}_kbs': 0 for app in app_cidrs.keys()}  # Create default values
#             update_device_traffic(device_mac, app_traffic_default)
#             app_traffic_default = {f'{app}_kbs': 2 for app in app_cidrs.keys()}  # Update to value 2
#             update_device_traffic(device_mac, app_traffic_default)




# @app.route('/')
# def index():
#     return "IntelliFirewall is up and running!"

# if __name__ == "__main__":
#     while True:
#         device_macs = get_device_macs()
#         print("Device MACs:", device_macs)
#         sniff(prn=calculate_traffic, store=0, iface="wlp0s20f3")
#         time.sleep(10)
