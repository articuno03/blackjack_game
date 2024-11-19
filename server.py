import socket
import selectors
import json
import types
from Client.clientUI import header  # Import header function

sel = selectors.DefaultSelector()
clients = {}
next_client_id = 1
# Initialize PlayerInfo instance
player_info = PlayerInfo()

def accept(sock):
    global next_client_id
    conn, addr = sock.accept()
    print("Accepted connection from", addr)
    conn.setblocking(False)
    client_id = next_client_id
    next_client_id += 1
    clients[conn] = {"addr": addr, "id": client_id, "username": None}
    sel.register(conn, selectors.EVENT_READ, read)
    
    # Send welcome message
    conn.send(header().encode())
    

def read(conn):
    try:
        data = conn.recv(1024)
        if data:
            message = json.loads(data.decode())
            handle_message(conn, message)
        else:
            close_connection(conn)
    except ConnectionResetError:
        close_connection(conn)

def handle_message(conn, message):
    if message["type"] == "join":
        username = message["content"]["username"]
        client_id = clients[conn]["id"]

        # Check if the username is already in use
        if not player_info.add_user(client_id, username):
            conn.send(json.dumps({"type": "error", "content": "Username already taken"}).encode())
            return

        clients[conn]["username"] = username
        broadcast_message({"type": "info", "content": f"Client {client_id} ({username}) has joined the game."})
    elif message["type"] == "chat":
        chat_message = {"username": clients[conn]['username'], "text": message['content']['text']}
        print(f"{chat_message['username']}: {chat_message['text']}")  # Display chat message on the server
        broadcast_message({"type": "chat", "content": chat_message})
    elif message["type"] == "quit":
        broadcast_message({"type": "info", "content": f"Client {clients[conn]['id']} ({clients[conn]['username']}) has left the game."})
        close_connection(conn)
    elif message["type"] == "list":
        # Handle list command to send back current users
        user_list = player_info.get_user_list()
        conn.send(json.dumps({"type": "info", "content": f"Connected users: {', '.join(user_list)}"}).encode())

def close_connection(conn):
    if conn in clients:
        username = clients[conn]["username"]
        player_info.remove_user(username)  # Remove from active users

        client_id = clients[conn]["id"]
        print('Closing connection to', clients[conn]["addr"])
        sel.unregister(conn)
        conn.close()
        del clients[conn]
        # Notify other clients
        broadcast_message({"type": "info", "content": f"Client {client_id} ({username}) has left the game."})

def broadcast_message(message):
    msg_data = json.dumps(message).encode()
    for conn in list(clients.keys()):
        try:
            conn.send(msg_data)
        except BrokenPipeError:
            close_connection(conn)

# Server Setup
host = '0.0.0.0'
port = 23456

sock = socket.socket()
sock.bind((host, port))
sock.listen(5)
print("Listening on", (host, port))
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
