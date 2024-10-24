import socket
import selectors
import json

sel = selectors.DefaultSelector()
clients = {}


def accept(sock, mask):
    conn, addr = sock.accept()  
    print('accepted connection from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    clients[conn] = {"addr": addr, "state": {}}

def read(conn, mask):
    data = conn.recv(1024)
    if data:
        message = json.loads(data.decode())
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()
        del clients[conn]

def proccess_message(conn, message):
    msg_type = message.get("type")
    if msg_type == "join":
        handle_join(conn, message)
    elif msg_type == "move":
        handle_move(conn, message)
    elif msg_type == "chat":
        handle_chat(conn, message)
    elif msg_type == "quit":
        handle_quit(conn, message)


def handle_join(conn, message):
    client_id = message["content"]["client_id"]
    clients[conn]["state"]["client_id"] = client_id
    print(f"Client {client_id} joined from {clients[conn]['addr']}")

def handle_move(conn, message):
    move_data = message["content"]
    clients[conn]["state"]["move"] = move_data
    print(f"Client {clients[conn]['state']['client_id']} moved: {move_data}")

def handle_chat(conn, message):
    chat_text = message["content"]["text"]
    print(f"Chat from {clients[conn]['state']['client_id']}: {chat_text}")

def handle_quit(conn, message):
    client_id = message["content"]["client_id"]
    print(f"Client {client_id} quit")
    sel.unregister(conn)
    conn.close()
    del clients[conn]
        
    
host = '0.0.0.0' 
port = 23456

sock = socket.socket()
sock.bind((host, port))
sock.listen(5)
print("listening on", (host, port))
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
