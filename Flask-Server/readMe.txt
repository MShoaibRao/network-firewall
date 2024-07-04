# IntelliFirewall Setup Guide

This guide provides step-by-step instructions to set up and run the IntelliFirewall project, which consists of a Flask server, a Node server, a React frontend, and a MongoDB database.

## Prerequisites

Make sure you have the following software installed on your system:

- **Python 3.x**: [Python Installation Guide](https://www.python.org/downloads/)
- **Node.js and npm**: [Node.js Installation Guide](https://nodejs.org/en/download/)
- **MongoDB**: [MongoDB Installation Guide](https://docs.mongodb.com/manual/installation/)

## Project Structure

intelliFirewall/
│
├── Flask-Server/
│ └── run.sh
│
├── Node-server/
│ └── (Node.js server files)
│
├── IntelliFirewall_frontEnd/
│ └── (React frontend files)
│
├── requirements.txt
└── Intellifirewall.sh


2. Install Python Dependencies:
	sudo pip install -r requirements.txt


3. Set Up Node.js and React:
	cd Node-server
	npm install

4. Navigate to the IntelliFirewall_frontEnd directory and create a React app (if not already created):

	cd ../IntelliFirewall_frontEnd
	npm install
	
	
5. Install and Start MongoDB:
	wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
	echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
	sudo apt update
	sudo apt install -y mongodb-org
	
	
6. Start Mongo:
	sudo service mongod start
	
7. Running the Project:
	chmod +x ./Intellifirewall.sh  (only once)
	./Intellifirewall.sh start
	./Intellifirewall.sh stop
	


