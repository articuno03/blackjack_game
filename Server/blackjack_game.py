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
        if self.current_player < len(self.turn_order):
            current_username = self.turn_order[self.current_player]
            self.broadcast({
                "type": "info",
                "content": f"It's {current_username}'s turn."
            })
        else:
            self.end_game()

    def end_game(self):
        self.broadcast({
            "type": "info",
            "content": "The game has ended. Calculating results..."
        })
        # Add result calculation and announce the winner

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

        elif action == "stand":
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
