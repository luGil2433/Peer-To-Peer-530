from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets for local communication

db_path = "p2p_data.db"

# Initialize the database
def init_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()

active_users = {}

@socketio.on("connect")
def handle_connect():
    print("A user connected.")

@socketio.on("register")
def register_user(data):
    username = data["username"]
    active_users[username] = request.sid
    join_room(username)
    print(f"{username} registered.")

@socketio.on("send_message")
def handle_message(data):
    sender = data["sender"]
    receiver = data["receiver"]
    content = data["content"]

    if receiver in active_users:
        emit("receive_message", data, room=receiver)
    else:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)",
                (sender, receiver, content),
            )
            conn.commit()

@socketio.on("fetch_messages")
def fetch_messages(data):
    user = data["username"]
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sender, receiver, content, timestamp FROM messages WHERE receiver = ? OR sender = ?",
            (user, user),
        )
        messages = cursor.fetchall()
    
    emit("message_history", {"messages": messages})

@socketio.on("disconnect")
def handle_disconnect():
    user_to_remove = None
    for user, sid in active_users.items():
        if sid == request.sid:
            user_to_remove = user
            break

    if user_to_remove:
        del active_users[user_to_remove]
        leave_room(user_to_remove)
        print(f"{user_to_remove} disconnected.")

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
