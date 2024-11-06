import socket
import selectors
import json
import types

sel = selectors.DefaultSelector()
clients = {}
next_client_id = 1

def accept(sock):
    global next_client_id
    conn, addr = sock.accept()
    print("Accepted connection from", addr)
    conn.setblocking(False)
    client_id = next_client_id
    next_client_id += 1
    clients[conn] = {"addr": addr, "id": client_id, "username": None}
    sel.register(conn, selectors.EVENT_READ, read)

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
        clients[conn]["username"] = message["content"]["username"]
        broadcast_message({"type": "info", "content": f"Client {clients[conn]['id']} ({clients[conn]['username']}) has joined the game."})
    elif message["type"] == "chat":
        chat_message = f"{clients[conn]['username']}: {message['content']['text']}"
        print(chat_message)  # Display chat message on the server
        broadcast_message({"type": "chat", "content": chat_message})
    elif message["type"] == "quit":
        broadcast_message({"type": "info", "content": f"Client {clients[conn]['id']} ({clients[conn]['username']}) has left the game."})
        close_connection(conn)

def close_connection(conn):
    if conn in clients:
        print('Closing connection to', clients[conn]["addr"])
        sel.unregister(conn)
        conn.close()
        del clients[conn]

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
