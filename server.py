import socket
import selectors
import json
import types
from Client.clientUI import header  # Import header function
from Server.player_info import PlayerInfo
from Server.blackjack_game import BlackjackGame

sel = selectors.DefaultSelector()
clients = {}
next_client_id = 1

ready_players = set() # Tracks player IDs who are ready
game_started = False
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
    global ready_players, game_started

    # Handle join message
    if message["type"] == "join":
        username = message["content"]["username"]
        
        # Ensure username is not already in use
        if player_info.add_user(clients[conn]["id"], username):
            clients[conn]["username"] = username  # Save username in clients dictionary
            print(f"Client {clients[conn]['id']} joined as {username}.")
            #conn.send(json.dumps({"type": "info", "content": f"Welcome, {username}!"}).encode())
            
            # Notify other clients
            broadcast_message({"type": "info", "content": f"{username} has joined the game."})
        else:
            # Username already taken
            conn.send(json.dumps({"type": "error", "content": "Username is already taken. Please try again."}).encode())
    
    # Handle start message
    elif message["type"] == "start":
        player_id = clients[conn]["id"]
        username = clients[conn]["username"]

        if game_started:
            conn.send(json.dumps({"type": "error", "content": "Game already in progress."}).encode())
            return

        # Add player to the ready queue
        ready_players.add(player_id)
        broadcast_message({"type": "info", "content": f"{username} is ready. ({len(ready_players)}/{len(clients)})"})

        # Check if all players are ready
        if len(ready_players) == len(clients):
            game_started = True  # Start the game
            broadcast_message({"type": "start", "content": "All players are ready! Starting the game..."})
            players = [{"conn": conn, "username": clients[conn]["username"]} for conn in clients]

            # Start the game using BlackjackGame class
            blackjack_game = BlackjackGame(players)
            blackjack_game.start_game()

    # Handle chat message
    elif message["type"] == "chat":
        chat_message = {"username": clients[conn]['username'], "text": message['content']['text']}
        print(f"{chat_message['username']}: {chat_message['text']}")  # Display chat message on the server
        broadcast_message({"type": "chat", "content": chat_message})

    # Handle list message
    elif message["type"] == "list":
        # Fetch connected users from PlayerInfo
        user_list = player_info.get_user_list()
        user_list_message = {
            "type": "list",
            "content": {"users": user_list}
        }
        conn.send(json.dumps(user_list_message).encode())

    # Handle quit message
    elif message["type"] == "quit":
        broadcast_message({"type": "info", "content": f"Client {clients[conn]['id']} ({clients[conn]['username']}) has left the game."})
        close_connection(conn)

def close_connection(conn):
    if conn in clients:
        username = clients[conn]["username"]

        # Remove the user from PlayerInfo if they have a username
        if username:
            player_info.remove_user(username)
            print(f"Removed {username} from player list.")

        client_id = clients[conn]["id"]
        print('Closing connection to', clients[conn]["addr"])
        sel.unregister(conn)
        conn.close()
        del clients[conn]
        # Notify other clients
        broadcast_message({"type": "info",
                            "content": f"Client {client_id} ({username}) has left the game."})

def broadcast_message(message):
    msg_data = json.dumps(message).encode()
    for conn in list(clients.keys()):
        try:
            conn.send(msg_data)
        except BrokenPipeError:
            close_connection(conn)

def start_game_logic():
    # Initialize the blackjack game
    print("Starting the blackjack game!")
    # add logic here to shuffle cards, deal initial hands, etc.
    # Example: Deal cards to all players
    for conn in clients:
        conn.send(json.dumps({"type": "game", "content": "Blackjack game started!"}).encode())

    # Reset readiness for the next game
    reset_game_state()

def reset_game_state():
    global ready_players, game_started
    ready_players.clear()
    game_started = False
    print("Game state reset. Ready for the next game.")


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
