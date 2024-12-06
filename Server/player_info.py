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
        self.players[client_id] = {"username": username, "money": 100}
        self.save_players()
        return True

    def remove_user(self, username):
        """Removes a user by username."""
        client_id = next((cid for cid, info in self.players.items() if info["username"] == username), None)
        if client_id is not None:
            del self.players[client_id]
            self.save_players()
            return True
        return False

    def get_user_list(self):
        """Returns a list of currently connected usernames."""
        return [info["username"] for info in self.players.values()]

    def get_user_money(self, username):
        """Returns the money of a user by username."""
        for info in self.players.values():
            if info["username"] == username:
                return info["money"]
        return None

    def update_user_money(self, username, amount):
        """Updates the money of a user by username."""
        for info in self.players.values():
            if info["username"] == username:
                info["money"] = amount
                self.save_players()
                return True
        return False

    def place_bet(self, username, amount):
        """Places a bet for a user."""
        for info in self.players.values():
            if info["username"] == username:
                if info["money"] >= amount:
                    info["money"] -= amount
                    info["bet"] = amount
                    self.save_players()
                    return True
                return False
        return False

    def resolve_bet(self, username, won):
        """Resolves a bet for a user."""
        for info in self.players.values():
            if info["username"] == username:
                if "bet" in info:
                    if won:
                        info["money"] += info["bet"] * 2.5  # 1.5 times the bet plus the original bet
                    info.pop("bet")
                    self.save_players()
                    return True
        return False