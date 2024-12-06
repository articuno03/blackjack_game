# FILE: player.py

class Player:
    def __init__(self, conn, username, money=100):
        self.conn = conn
        self.username = username
        self.money = money

    def add_money(self, amount):
        self.money += amount

    def subtract_money(self, amount):
        if amount <= self.money:
            self.money -= amount
            return True
        return False

    def get_money(self):
        return self.money

    def __repr__(self):
        return f"Player(username={self.username}, money={self.money})"