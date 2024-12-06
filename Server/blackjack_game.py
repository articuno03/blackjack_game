import json
import random
import src.ui as UI
from .player_info import PlayerInfo

class BlackjackGame:
    def __init__(self, players, broadcast_callback, end_game_callback):
        """
        Initialize the game.
        :param players: List of player dictionaries with their connection and username.
        :param broadcast_callback: A callback function to broadcast messages to all players.
        :param end_game_callback: A callback function to notify the server that the game has ended.
        """
        self.players = players
        self.broadcast = broadcast_callback
        self.end_game_callback = end_game_callback
        self.deck = self.create_deck()
        self.hands = {player['username']: [] for player in players}
        self.hands['Dealer'] = []
        self.turn_order = [player['username'] for player in players] + ['Dealer']
        self.current_player = 0
        self.busted_players = set()
        self.finished_players = set()
        self.player_info = PlayerInfo()  # Create an instance of PlayerInfo

    def create_deck(self):
        suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
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
        self.hands['Dealer'] = [self.deck.pop()]

    def send_hand(self, conn, username):
        hand = self.hands[username]
        opponent_cards = {}

        for opponent in self.hands:
            if opponent != username and len(self.hands[opponent]) > 0:
                opponent_cards[opponent] = self.hands[opponent]

        conn.send(json.dumps({
            "type": "game",
            "content": {
                "scoreboard": UI.topScoreboard(),
                "your_hand": UI.userScoreboard(hand),
                "opponentsUI": UI.opponentScoreboard(),
                "opponents": {opponent: ', '.join(cards) for opponent, cards in opponent_cards.items()},
                "bottom": UI.bottomScoreboard()
            }

        }).encode())

    def start_game(self):
        self.deal_initial_cards()
        self.prompt_bets()

    def prompt_bets(self):
        for player in self.players:
            conn, username = player['conn'], player['username']
            conn.send(json.dumps({
                "type": "info",
                "content": "Place your bet."
            }).encode())

    def handle_player_bet(self, conn, amount):
        username = self.turn_order[self.current_player]
        if self.player_info.place_bet(username, amount):
            self.broadcast({
                "type": "info",
                "content": f"{username} placed a bet of {amount}."
            })
            self.send_hand(conn, username)  # Send the updated scoreboard to the player
            self.current_player += 1
            if self.current_player >= len(self.turn_order) - 1:
                self.current_player = 0
                self.prompt_next_player()
        else:
            conn.send(json.dumps({
                "type": "error",
                "content": "Insufficient funds or invalid bet."
            }).encode())

    def prompt_next_player(self):
        # Skip players who have busted or finished their turn
        while self.current_player < len(self.turn_order) and \
                (self.turn_order[self.current_player] in self.busted_players or
                 self.turn_order[self.current_player] in self.finished_players):
            self.current_player += 1

        if self.current_player < len(self.turn_order):
            current_username = self.turn_order[self.current_player]
            if current_username == 'Dealer':
                self.dealer_turn()
            else:
                self.broadcast({
                    "type": "info",
                    "content": f"It's {current_username}'s turn."
                })
        else:
            self.dealer_turn()

    def dealer_turn(self):
        dealer_hand = self.hands['Dealer']
        while self.calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(self.deck.pop())
        if self.calculate_hand_value(dealer_hand) > 21:
            self.broadcast({
                "type": "info",
                "content": "Dealer busted!"
            })
            self.busted_players.add('Dealer')
        self.finished_players.add('Dealer')
        self.broadcast_dealer_hand()
        self.end_game()

    def broadcast_dealer_hand(self):
        dealer_hand = self.hands['Dealer']
        self.broadcast({
            "type": "info",
            "content": f"Dealer's final hand: {', '.join(dealer_hand)}"
        })

    def end_game(self):
        results = []
        dealer_value = self.calculate_hand_value(self.hands['Dealer'])
        for username, hand in self.hands.items():
            if username != 'Dealer':
                hand_value = self.calculate_hand_value(hand)
                if hand_value > 21 or (dealer_value <= 21 and dealer_value >= hand_value):
                    self.player_info.resolve_bet(username, False)
                else:
                    self.player_info.resolve_bet(username, True)
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

        self.end_game_callback()  # Notify the server that the game has ended

    def handle_player_action(self, conn, action):
        username = self.turn_order[self.current_player]

        if action == "hit":
            card = self.deck.pop()
            self.hands[username].append(card)
            self.send_hand(conn, username)  # Send the updated hand to the player

            # Print the updated hand to the terminal
            print(f"\n{username}'s updated hand: {', '.join(self.hands[username])}\n")

            if self.calculate_hand_value(self.hands[username]) > 21:
                self.busted_players.add(username)
                self.broadcast({
                    "type": "info",
                    "content": f"{username} busted!"
                })
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

    def __repr__(self):
        return UI.scoreboard(self.players)
