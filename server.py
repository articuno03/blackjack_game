import socket
import selectors
import json
from Server.player_info import PlayerInfo
from Server.blackjack_game import BlackjackGame

sel = selectors.DefaultSelector()
clients = {}
ready_players = set()
game_started = False
player_info = PlayerInfo()

blackjack_game = None  # Store the game instance


def accept(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    client_id = len(clients) + 1
    clients[conn] = {"addr": addr, "id": client_id, "username": None}
    sel.register(conn, selectors.EVENT_READ, read)
    conn.send(header().encode())
    print(f"Accepted connection from {addr}")


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
    global ready_players, game_started, blackjack_game

    message_type = message["type"]

    if message_type == "join":
        handle_join(conn, message)

    elif message_type == "start":
        handle_start(conn)

    elif message_type == "chat":
        broadcast_message({
            "type": "chat",
            "content": {
                "username": clients[conn]["username"],
                "text": message["content"]["text"],
            }
        })

    elif message_type == "list":
        send_player_list(conn)

    elif message_type == "quit":
        close_connection(conn)

    elif message_type == "game":
        if blackjack_game and game_started:
            blackjack_game.handle_player_action(conn, message["content"])


def handle_join(conn, message):
    username = message["content"]["username"]

    if player_info.add_user(clients[conn]["id"], username):
        clients[conn]["username"] = username
        broadcast_message({"type": "info", "content": f"{username} has joined the game."})
    else:
        conn.send(json.dumps({"type": "error", "content": "Username is already taken."}).encode())


def handle_start(conn):
    global ready_players, game_started, blackjack_game

    if game_started:
        conn.send(json.dumps({"type": "error", "content": "Game already in progress."}).encode())
        return

    player_id = clients[conn]["id"]
    username = clients[conn]["username"]
    ready_players.add(player_id)

    broadcast_message({
        "type": "info",
        "content": f"{username} is ready. ({len(ready_players)}/{len(clients)})"
    })

    if len(ready_players) == len(clients):
        game_started = True
        broadcast_message({"type": "start", "content": "All players are ready! Starting the game..."})

        players = [{"conn": conn, "username": clients[conn]["username"]} for conn in clients]
        blackjack_game = BlackjackGame(players, broadcast_message)
        blackjack_game.start_game()


def send_player_list(conn):
    user_list = player_info.get_user_list()
    conn.send(json.dumps({"type": "list", "content": {"users": user_list}}).encode())


def close_connection(conn):
    if conn in clients:
        username = clients[conn]["username"]
        if username:
            player_info.remove_user(username)
            print(f"{username} has disconnected.")
        sel.unregister(conn)
        conn.close()
        del clients[conn]
        broadcast_message({"type": "info", "content": f"{username} has left the game."})


def broadcast_message(message):
    for conn in clients:
        try:
            conn.send(json.dumps(message).encode())
        except BrokenPipeError:
            close_connection(conn)


def header():
    return '''\
===================================================================
                       Welcome to Blackjack       
===================================================================
Commands:
  start - Join the game queue
  chat  - Chat with other players
  list  - Show connected players
  quit  - Leave the game
===================================================================
'''


# Server setup
host = '0.0.0.0'
port = 23456

sock = socket.socket()
sock.bind((host, port))
sock.listen(5)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

print(f"Server is listening on {host}:{port}")

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    sel.close()
