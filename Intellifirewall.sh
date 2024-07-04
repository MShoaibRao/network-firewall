#!/bin/bash

# Function to start services
start_services() {
    # Start MongoDB service
    echo "Starting MongoDB service..."
    sudo service mongod start
    if [ $? -ne 0 ]; then
        echo "Failed to start MongoDB service. Exiting..."
        exit 1
    fi

    # Start Flask-Server
    echo "Starting Flask-Server..."
    (cd Flask-Server && ./run.sh) &
    FLASK_PID=$!
    if [ $? -ne 0 ]; then
        echo "Failed to start Flask-Server. Exiting..."
        exit 1
    fi

    # Start Node-server
    echo "Starting Node-server..."
    (cd Node-server && npm start) &
    NODE_PID=$!
    if [ $? -ne 0 ]; then
        echo "Failed to start Node-server. Exiting..."
        exit 1
    fi

    # Start IntelliFirewall_frontEnd
    echo "Starting IntelliFirewall_frontEnd..."
    (cd IntelliFirewall_frontEnd && npm start) &
    FRONTEND_PID=$!
    if [ $? -ne 0 ]; then
        echo "Failed to start IntelliFirewall_frontEnd. Exiting..."
        exit 1
    fi

    # Wait for all processes to exit
    echo "All services started. Press [CTRL+C] to stop."
    wait $FLASK_PID $NODE_PID $FRONTEND_PID
}

# Function to stop services
stop_services() {
    echo "Stopping all services..."

    # Stopping MongoDB service
    echo "Stopping MongoDB service..."
    sudo service mongod stop
    if [ $? -ne 0 ]; then
        echo "Failed to stop MongoDB service."
    fi

    # Killing background processes
    if [ -n "$FLASK_PID" ]; then
        echo "Stopping Flask-Server..."
        kill $FLASK_PID
    fi

    if [ -n "$NODE_PID" ]; then
        echo "Stopping Node-server..."
        kill $NODE_PID
    fi

    if [ -n "$FRONTEND_PID" ]; then
        echo "Stopping IntelliFirewall_frontEnd..."
        kill $FRONTEND_PID
    fi

    echo "All services stopped."
}

# Function to display usage information
usage() {
    echo "Usage: $0 {start|stop}"
    exit 1
}

# Check command-line arguments
if [ $# -ne 1 ]; then
    usage
fi

case $1 in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    *)
        usage
        ;;
esac

# Handle cleanup on exit
trap "stop_services; exit" SIGINT SIGTERM

