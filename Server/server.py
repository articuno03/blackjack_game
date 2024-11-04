import socket
import selectors
import json

sel = selectors.DefaultSelector()
clients = {}

def accept(sock, mask):
    conn, addr = sock.accept()  
    print('Accepted connection from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    clients[conn] = {"addr": addr, "state": {}}

def read(conn, mask):
    try:
        data = conn.recv(1024)
        if data:
            # Decode and process incoming JSON data
            message = json.loads(data.decode())
            print("Received:", message, "from", clients[conn]["addr"])
            process_message(conn, message)
        else:
            # Client has disconnected
            close_connection(conn)
    except ConnectionResetError:
        close_connection(conn)

def process_message(conn, message):
    msg_type = message.get("type")
    if msg_type == "join":
        handle_join(conn, message)
    elif msg_type == "start":
        handle_start(conn, message)
    elif msg_type == "chat":
        handle_chat(conn, message)
    elif msg_type == "quit":
        handle_quit(conn, message)
    else:
        print(f"Unknown message type {msg_type} from {clients[conn]['addr']}")

def handle_join(conn, message):
    client_id = message["content"]["client_id"]
    username = message["content"]["username"]
    clients[conn]["state"]["client_id"] = client_id
    clients[conn]["state"]["username"] = username
    print(f" {username} joined from {clients[conn]['addr']}")
    broadcast_message({"type": "info", "content": f"Client {username} has joined the game."})
    # Assign each player with a unique ID
    # Prompt user for a username that will be associated with them for the entire game unitl they quit

def handle_start(conn, message):
    move_data = message["content"]
    clients[conn]["state"]["start"] = move_data
    print(f"Client {clients[conn]['state']['client_id']} start game: {move_data}")
    # This will begin the game, when any client enters start.
    # Use the GameBoard Class to send Board to all players

def handle_chat(conn, message):
    chat_text = message["content"]["text"]
    client_id = clients[conn]["state"].get("client_id", "Unknown")
    username = clients[conn]["state"]["username"]
    print(f"Chat from {username}: {chat_text}")
    # Broadcast the chat message to all clients
    broadcast_message({"type": "chat", "content": {"text": chat_text, "client_id": client_id}})

def handle_quit(conn, message):
    client_id = message["content"]["client_id"]
    print(f"Client {client_id} quit")
    broadcast_message({"type": "info", "content": f"Client {client_id} has left the game."})
    close_connection(conn)

def close_connection(conn):
    """Helper to clean up a client connection."""
    print('Closing connection to', clients[conn]["addr"])
    sel.unregister(conn)
    conn.close()
    del clients[conn]

def broadcast_message(message):
    """Broadcasts a JSON message to all connected clients."""
    msg_data = json.dumps(message).encode()
    for conn in clients:
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
            callback(key.fileobj, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
