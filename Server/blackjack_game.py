import json

class BlackjackGame:
    def __init__(self, players):
        """
        Initialize the game with a list of players.
        :param players: List of player dictionaries with their connection and username.
        """
        self.players = players
        self.deck = self.create_deck()  # Initialize a deck of cards
        self.hands = {player['username']: [] for player in players}  # Store player hands

    def create_deck(self):
        """Creates a standard 52-card deck."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [f"{rank} of {suit}" for suit in suits for rank in ranks]

    def shuffle_deck(self):
        """Shuffles the deck."""
        import random
        random.shuffle(self.deck)

    def deal_initial_cards(self):
        """Deals two cards to each player."""
        self.shuffle_deck()
        for player in self.players:
            username = player['username']
            self.hands[username] = [self.deck.pop(), self.deck.pop()]

    def send_initial_hands(self):
        """Sends each player their own cards."""
        for player in self.players:
            conn = player['conn']
            username = player['username']
            hand = self.hands[username]
            try:
                conn.send(json.dumps({
                    "type": "game",
                    "content": f"Your initial hand: {', '.join(hand)}"
                }).encode())
                print(f"Sent hand to {username}: {', '.join(hand)}")
            except BrokenPipeError:
                print(f"Failed to send hand to {username}. Connection might be closed.")

    def broadcast_game_start(self):
        """Notify players that the game has started and send initial hands."""
        for player in self.players:
            conn = player['conn']
            username = player['username']
            conn.send(json.dumps({
                "type": "game",
                "content": f"Game started! Your hand: {self.hands[username]}"
            }).encode())

    def start_game(self):
        """Starts the game logic."""
        print("Blackjack game is starting...")
        self.deal_initial_cards()
        self.broadcast_game_start()

        # You can add more logic for gameplay here.
