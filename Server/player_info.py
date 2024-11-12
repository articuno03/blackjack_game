# player_info.py

import json
import os

class PlayerInfo:
    def __init__(self, file_path="players.json"):
        self.file_path = file_path
        self.players = self.load_players()

    def load_players(self):
        """Load players from the JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def save_players(self):
        """Save players to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.players, f)

    def add_user(self, client_id, username):
        """Add a new user if the username is unique."""
        if username in self.players.values():
            return False  # Username already taken
        self.players[client_id] = username
        self.save_players()
        return True

    def remove_user(self, username):
        """Remove a user by their username."""
        client_id = None
        for id, name in list(self.players.items()):
            if name == username:
                client_id = id
                del self.players[client_id]
                break
        self.save_players()
        return client_id is not None

    def get_user_list(self):
        """Return a list of currently connected usernames."""
        return list(self.players.values())
