# import subprocess
# import time
# import psutil
# from pymongo import MongoClient

# # Function to calculate network speed
# def get_network_speed():
#     # Get the number of bytes sent and received over the network
#     bytes_sent = psutil.net_io_counters().bytes_sent
#     bytes_received = psutil.net_io_counters().bytes_recv
    
#     # Wait for 10 seconds
#     time.sleep(10)
    
#     # Get the new number of bytes sent and received after 10 seconds
#     new_bytes_sent = psutil.net_io_counters().bytes_sent
#     new_bytes_received = psutil.net_io_counters().bytes_recv
    
#     # Calculate the total number of bytes sent and received in 10 seconds
#     total_bytes_sent = new_bytes_sent - bytes_sent
#     total_bytes_received = new_bytes_received - bytes_received
    
#     # Calculate the network speed in bytes per second
#     net_speed_bytes_per_sec = (total_bytes_sent + total_bytes_received) / 10
    
#     # Convert bytes per second to bits per second (8 bits in a byte)
#     net_speed_bits_per_sec = net_speed_bytes_per_sec * 8
    
#     # Return the network speed in bits per second
#     return net_speed_bits_per_sec

# # Function to get the number of connected devices
# def get_connected_devices(interface):
#     try:
#         # Run the arp command to get the list of devices connected to the specified interface
#         arp_output = subprocess.check_output('arp -a | awk \'{print $4}\'', shell=True)
#         # Split the output into lines and count the number of MAC addresses
#         mac_addresses = arp_output.decode().split('\n')
#         # Remove any empty lines
#         mac_addresses = [mac for mac in mac_addresses if mac]
#         num_connected_devices = len(mac_addresses)
#         return num_connected_devices
#     except subprocess.CalledProcessError as e:
#         print("Error:", e)
#         return 0

# # Function to update MongoDB data
# # def update_mongodb_data(speed, connected_devices):
# #     client = MongoClient('mongodb://localhost:27017/')
# #     db = client['IntelliFirewall']
# #     collection = db['dasboard_items']
# #     collection.update_one({}, {'$set': {'Traffic_Speed': (speed/1024), 'Connected_devices': connected_devices}})

# from datetime import datetime, timedelta

# # Function to update MongoDB data including line graph data for every minute
# def update_mongodb_data(speed, connected_devices):
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['IntelliFirewall']
#     collection = db['dasboard_items']
#     line_chart_collection = db['line_charts']  # Collection for line chart data
    
#     # Update dasboard_items collection
#     collection.update_one({}, {'$set': {'Traffic_Speed': (speed/1024), 'Connected_devices': connected_devices}})
    
#     # Get current minute with seconds
#     current_time = datetime.now().strftime('%I:%M:%S %p')
#     current_minute = datetime.now().strftime('%I:%M:%S %p')
    
#     # Remove data older than 10 minutes
#     oldest_allowed_time = (datetime.now() - timedelta(minutes=3)).strftime('%I:%M:%S %p')
#     line_chart_collection.delete_many({'data.x': {'$lt': oldest_allowed_time}})
    
#     # Update line chart data for every minute
#     line_chart_collection.update_one(
#         {'Line': 'InternetSpeed'},  # Search for existing data for the InternetSpeed line
#         {'$push': {'data': {'x': current_time, 'y': speed/1024}}},  # Add internet speed for the current minute
#         upsert=True  # If no data exists for the InternetSpeed line, insert a new document
#     )







# # Main function
# def main():
#     interface = 'wlp0s20f3'  # Interface name
#     while True:
#         # Calculate network speed
#         speed = get_network_speed()
#         print("Traffic_Speed:", (speed/1024))
        
#         # Get the number of connected devices
#         connected_devices = get_connected_devices(interface)
#         print("Connected_devices:", connected_devices)
        
#         # Update MongoDB data
#         update_mongodb_data((speed/1024), connected_devices)
        
#         # Wait for 10 seconds before the next iteration
#         time.sleep(10)

# if __name__ == "__main__":
#     main()



# ////////////////////////////////////////////////////////


import subprocess
import time
import psutil
from pymongo import MongoClient
from datetime import datetime, timedelta

# Function to calculate network speed
def get_network_speed():
    # Get the number of bytes sent and received over the network
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_received = psutil.net_io_counters().bytes_recv
    
    # Wait for 10 seconds
    time.sleep(10)
    
    # Get the new number of bytes sent and received after 10 seconds
    new_bytes_sent = psutil.net_io_counters().bytes_sent
    new_bytes_received = psutil.net_io_counters().bytes_recv
    
    # Calculate the total number of bytes sent and received in 10 seconds
    total_bytes_sent = new_bytes_sent - bytes_sent
    total_bytes_received = new_bytes_received - bytes_received
    
    # Calculate the network speed in bytes per second
    net_speed_bytes_per_sec = (total_bytes_sent + total_bytes_received) / 10
    
    # Convert bytes per second to bits per second (8 bits in a byte)
    net_speed_bits_per_sec = net_speed_bytes_per_sec * 8
    
    # Return the network speed in bits per second
    return net_speed_bits_per_sec

# Function to get the number of connected devices
def get_connected_devices(interface):
    try:
        # Run the arp command to get the list of devices connected to the specified interface
        arp_output = subprocess.check_output('arp -a | awk \'{print $4}\'', shell=True)
        # Split the output into lines and count the number of MAC addresses
        mac_addresses = arp_output.decode().split('\n')
        # Remove any empty lines
        mac_addresses = [mac for mac in mac_addresses if mac]
        num_connected_devices = len(mac_addresses)
        return num_connected_devices
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return 0

# Function to update MongoDB data including line graph data for every minute
def update_mongodb_data(speed, connected_devices):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['IntelliFirewall']
    collection = db['dasboard_items']
    line_chart_collection = db['line_charts']  # Collection for line chart data
    
    # Update dasboard_items collection
    collection.update_one({}, {'$set': {'Traffic_Speed': (speed/1024), 'Connected_devices': connected_devices}})
    
    # Get current minute
    current_minute = datetime.now().strftime('%H:%M')
    
    # Remove data older than 10 minutes
    oldest_allowed_time = (datetime.now() - timedelta(minutes=12)).strftime('%H:%M')
    line_chart_collection.update_one(
        {'Line': 'InternetSpeed'},
        {'$pull': {'data': {'x': {'$lt': oldest_allowed_time}}}}
    )
    
    # Update line chart data for every minute
    line_chart_collection.update_one(
        {'Line': 'InternetSpeed'},  # Search for existing data for the InternetSpeed line
        {'$push': {'data': {'x': current_minute, 'y': speed/1024}}},  # Add internet speed for the current minute
        upsert=True  # If no data exists for the InternetSpeed line, insert a new document
    )



# Main function
def main():
    interface = 'wlp0s20f3'  # Interface name
    while True:
        # Calculate network speed
        speed = get_network_speed()
        print("Traffic_Speed:", (speed/1024))
        
        # Get the number of connected devices
        connected_devices = get_connected_devices(interface)
        print("Connected_devices:", connected_devices)
        
        # Update MongoDB data
        update_mongodb_data((speed/1024), connected_devices)
        
        # Wait for 1 minute before the next iteration
        time.sleep(60)

if __name__ == "__main__":
    main()
