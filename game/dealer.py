from random import *

from .game import Game
from .dealerInterface import DealerInterface
from .hand import Hand
from .handInterface import HandInterface
from .card import Card
from .cardInterface import CardInterface
from .trick import Trick
from .trickInterface import TrickInterface

class Dealer(DealerInterface):

    def create_game(self, number_of_players: int) -> Game:
        cards = [
            "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
        ]

        card_stack = []
        for i in range(4): # 4 suits
            for card in cards:
                card_stack.append(card)

        shuffle(card_stack)

        trick_itf: TrickInterface = Trick()
        hands = []
        for i in range(number_of_players): # 2-4 players
            hand = []
            for o in range(6): # 6 cards in hand
                card_itf: CardInterface = Card(card_stack.pop())
                hand.append(card_itf)
            hand_itf: HandInterface = Hand(hand, trick_itf)
            hands.append(hand_itf)

        game = Game(3, 0, hands, trick_itf)
        return game
