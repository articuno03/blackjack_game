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
        username = input(f"Enter username for connection {conn_id}: ").strip()

        data = types.SimpleNamespace(
            username=username,
            conn_id=conn_id,
            recv_total=0,
            outb=b"",
            messages=[create_message("join", {"username": username})],
            chat_mode=False,  # Initialize chat mode as False
        )
        sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

        # Start a separate thread to get user input
        threading.Thread(target=get_user_input, args=(data,)).start()


def create_message(msg_type, content):
    """Creates a JSON message with a specified type and content."""
    return json.dumps({"type": msg_type, "content": content}).encode()


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            try:
                message = json.loads(recv_data.decode())
                handle_message(data, message)
            except json.JSONDecodeError:
                print(recv_data.decode())
        else:
            print("Connection closed by server.")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


def handle_message(data, message):
    """Processes incoming server messages."""
    msg_type = message["type"]
    content = message.get("content", "")

    if msg_type == "info":
        print(content)

    elif msg_type == "error":
        print(f"Error: {content}")

    elif msg_type == "start":
        print(f"Game: {content}")

    elif msg_type == "game":
        if isinstance(content, dict):  # Check if content is structured
            print(content["your_hand"])
            if "opponents" in content:
                print("Revealed Cards:")
                for opponent, card_info in content["opponents"].items():
                    print(f"  {opponent}: {card_info}")
        else:
            print(f"Game Update: {content}")

    elif msg_type == "chat":
        username, text = content["username"], content["text"]
        print(f"{username}: {text}")

    elif msg_type == "list":
        users = content.get("users", [])
        print("Connected users:", ", ".join(users))


def get_user_input(data):
    """Prompts the user for input commands."""
    while True:
        if data.chat_mode:
            text = input("Chat (type 'exit_chat' to leave): ")
            if text.lower() == "exit_chat":
                data.chat_mode = False
            else:
                # Send chat messages
                data.messages.append(create_message("chat", {"text": text}))
        else:
            command = input("Enter command (chat, start, list, hit, stand, quit): ").strip().lower()
            if command == "chat":
                data.chat_mode = True
            elif command == "start":
                data.messages.append(create_message("start", {}))
            elif command == "list":
                data.messages.append(create_message("list", {}))
            elif command == "hit":
                # Send a "game" message with the action "hit"
                data.messages.append(create_message("game", {"action": "hit"}))
            elif command == "stand":
                # Send a "game" message with the action "stand"
                data.messages.append(create_message("game", {"action": "stand"}))
            elif command == "quit":
                data.messages.append(create_message("quit", {}))
                return  # Quit the loop and exit
            else:
                print("Invalid command. Try again.")



# Main client logic
host = '0.0.0.0'
port = 23456
num_conns = 1  # Adjust for multiple connections

start_connections(host, port, num_conns)

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
