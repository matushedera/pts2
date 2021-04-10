from random import *

from .game import Game
from .dealerInterface import DealerInterface
from .hand import Hand
from .card import Card
from .trick import Trick

class Dealer:

    def create_game(self, number_of_players: int) -> Game:
        cards = [
            "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
        ]

        card_stack = []
        for i in range(4): # 4 suits
            for card in cards:
                card_stack.append(card)

        shuffle(card_stack)

        hands = []
        for i in range(number_of_players): # 2-4 players
            hand = []
            for o in range(6): # 6 cards in hand
                hand.append(Card(card_stack.pop()))
            hands.append(hand)

        trick = Trick()
        game = Game(3, 0, hands, trick)
        return game
