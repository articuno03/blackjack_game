import socket
import types
import selectors
import json
import threading

sel = selectors.DefaultSelector()

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(num_conns):
        conn_id = i + 1
        print("Starting connection", conn_id, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        try:
            sock.connect_ex(server_addr)
        except BlockingIOError:
            pass  # Connection is in progress
        
        # Prompt user for a username
        username = input(f"Enter username for connection {conn_id}: ")

        data = types.SimpleNamespace(
            username=username,
            conn_id=conn_id,
            recv_total=0,
            outb=b"",
            messages=[create_message("join", {"client_id": conn_id, "username": username})],  # Join message with username
            chat_mode=False # Initialize chat mode as False
        )
        sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

        # Start a separate thread to get user input for each connection
        input_thread = threading.Thread(target=get_user_input, args=(data,))
        input_thread.daemon = True
        input_thread.start()

def create_message(msg_type, content):
    """Creates a JSON message with a specified type and content."""
    message = {
        "type": msg_type,
        "content": content,
         
    }
    return json.dumps(message).encode()

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            message = json.loads(recv_data.decode())
           # print("Received", message, "from connection", data.conn_id)
            print(message["content"]) 
            data.recv_total += len(recv_data)
            handle_message(data, message)  # Process the received message
        if not recv_data:
            print("Closing connection", data.conn_id)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("Sending", repr(data.outb), "to connection", data.conn_id)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def handle_message(data, message):
    """Handles incoming messages from the server."""
    if message["type"] == "chat":
        data.chat_mode = True
        print("Chat mode enabled. You may now enter messages.")
    elif message["type"] == "start":
        print("Game start message:", message["content"])
    elif message["type"] == "quit":
        print("Player left the game:", message["content"]["client_id"])

def get_user_input(data):
    """Continuously prompt user to enter 'chat' to start chat mode."""
    while True:
        if data.chat_mode:
            # In chat mode, prompt for chat messages
            chat_text = input("Enter chat message (type 'exit_chat' to leave chat mode): ")
            if chat_text.lower() == "exit_chat":
                data.chat_mode = False  # Exit chat mode
                print("Exiting chat mode.")
            elif chat_text.lower() == "quit":
                data.messages.append(create_message("quit", {"client_id": data.conn_id}))
                break
            else:
                # Send chat message
                data.messages.append(create_message("chat", {"text": chat_text}))
        else:
            # When not in chat mode, prompt only once to enter "chat" or "quit"
            command = input("Enter 'chat' to start chat mode or 'quit' to disconnect: ")
            if command.lower() == "chat":
                data.chat_mode = True  # Enable chat mode
                print("Entering chat mode. You can now send messages.")
            elif command.lower() == "quit":
                data.messages.append(create_message("quit", {"client_id": data.conn_id}))
                break

# Main
host = '0.0.0.0'
port = 2345
num_conns = 1  # Adjust as needed

start_connections(host, port, num_conns)

# Event Loop
try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
