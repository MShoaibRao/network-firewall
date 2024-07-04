#!/bin/bash

# Run deviceAppTraffic.py
echo "Running deviceAppTraffic.py..."
sudo python3 deviceAppTraffic.py &




# Wait for 10 seconds
sleep 1

# Run Dashboard.py
echo "Running Dashboard.py..."
sudo python3 pieChart.py &



# Wait for 10 seconds
sleep 1

# Run mydb.py
echo "Running mydb.py..."
sudo python3 mydb.py &




#Running Blocking
sleep 1
echo "Running Blocking ...."
sudo python3 blockIP_api.py &



sleep 1
echo "Running Net Speed"
sudo python3 netSpeed.py

