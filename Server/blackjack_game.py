import json

class BlackjackGame:
    def __init__(self, players, broadcast_callback):
        """
        Initialize the game.
        :param players: List of player dictionaries with their connection and username.
        :param broadcast_callback: A callback function to broadcast messages to all players.
        """
        self.players = players
        self.broadcast = broadcast_callback
        self.deck = self.create_deck()
        self.hands = {player['username']: [] for player in players}
        self.turn_order = [player['username'] for player in players]
        self.current_player = 0
        self.busted_players = set()
        self.finished_players = set()

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [f"{rank} of {suit}" for suit in suits for rank in ranks]

    def shuffle_deck(self):
        import random
        random.shuffle(self.deck)

    def deal_initial_cards(self):
        self.shuffle_deck()
        for player in self.players:
            username = player['username']
            self.hands[username] = [self.deck.pop(), self.deck.pop()]

    def send_hand(self, conn, username):
        hand = self.hands[username]
        conn.send(json.dumps({
            "type": "game",
            "content": f"Your hand: {', '.join(hand)}"
        }).encode())

    def start_game(self):
        self.deal_initial_cards()
        for player in self.players:
            conn, username = player['conn'], player['username']
            self.send_hand(conn, username)
        self.prompt_next_player()

    def prompt_next_player(self):
        # Skip players who have busted or finished their turn
        while self.current_player < len(self.turn_order) and \
                (self.turn_order[self.current_player] in self.busted_players or
                 self.turn_order[self.current_player] in self.finished_players):
            self.current_player += 1

        if self.current_player < len(self.turn_order):
            current_username = self.turn_order[self.current_player]
            self.broadcast({
                "type": "info",
                "content": f"It's {current_username}'s turn."
            })
        else:
            self.end_game()

    def end_game(self):
        results = []
        for username, hand in self.hands.items():
            if username not in self.busted_players:
                hand_value = self.calculate_hand_value(hand)
                results.append((username, hand_value))
        results.sort(key=lambda x: x[1], reverse=True)

        winner = results[0][0] if results else None
        if winner:
            self.broadcast({
                "type": "info",
                "content": f"The game has ended. The winner is {winner} with a hand value of {results[0][1]}!"
            })
        else:
            self.broadcast({
                "type": "info",
                "content": "The game has ended. No winners, everyone busted!"
            })

    def handle_player_action(self, conn, action):
        username = self.turn_order[self.current_player]

        if action == "hit":
            card = self.deck.pop()
            self.hands[username].append(card)
            self.send_hand(conn, username)

            if self.calculate_hand_value(self.hands[username]) > 21:
                self.busted_players.add(username)
                conn.send(json.dumps({
                    "type": "info",
                    "content": "You busted!"
                }).encode())
                self.current_player += 1
                self.prompt_next_player()
            else:
                self.broadcast({
                    "type": "info",
                    "content": f"{username} chose to hit and received {card}."
                })

        elif action == "stand":
            self.finished_players.add(username)
            self.broadcast({
                "type": "info",
                "content": f"{username} chose to stand."
            })
            self.current_player += 1
            self.prompt_next_player()

    def calculate_hand_value(self, hand):
        value = 0
        aces = 0

        for card in hand:
            rank = card.split(' ')[0]
            if rank.isdigit():
                value += int(rank)
            elif rank in ['J', 'Q', 'K']:
                value += 10
            elif rank == 'A':
                value += 11
                aces += 1

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value
