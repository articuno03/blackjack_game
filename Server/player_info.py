import json
import os


class PlayerInfo:
    def __init__(self, file_path="players.json"):
        self.file_path = file_path
        self.players = self.load_players()

    def load_players(self):
        """Load players from a JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error: Corrupted players.json file. Resetting.")
                return {}
        return {}

    def save_players(self):
        """Save players to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.players, f)

    def add_user(self, client_id, username):
        """Adds a user if the username is unique."""
        if username in self.players.values():
            return False  # Username already taken
        self.players[client_id] = username
        self.save_players()
        return True

    def remove_user(self, username):
        """Removes a user by username."""
        client_id = next((cid for cid, uname in self.players.items() if uname == username), None)
        if client_id is not None:
            del self.players[client_id]
            self.save_players()
            return True
        return False

    def get_user_list(self):
        """Returns a list of currently connected usernames."""
        return list(self.players.values())
