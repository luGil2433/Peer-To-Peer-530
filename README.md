# Local Peer-to-Peer Chat System

This is a simple local chat application using **Flask-SocketIO** and **SQLite**. Messages are sent instantly if the recipient is online or stored in the database if they are offline.

## Features
- Local peer-to-peer messaging (runs on your computer, no internet needed).
- Real-time messaging with WebSockets.
- Offline message storage (messages are saved if the recipient is offline).
- Simple web-based client.

## Installation

1. Install Python dependencies:
```bash
pip install flask flask-socketio eventlet sqlite3
```

2. Start the server:

```bash
  python server.py
```
The server runs on http://localhost:5000.

3. Open index.html in a browser and register a username to start chatting.

## How It Works
1. The server runs locally and handles user connections.

2. Users register with a username.

3. Messages are sent instantly if the recipient is online.

4. Offline messages are stored in a database and delivered when the recipient reconnects.

