from typing import List

from .handInterface import HandInterface
from .gameInterface import GameInterface
from .trickInterface import TrickInterface

class Game(GameInterface):

    def __init__(self, number_of_players: int, trick_started_by: int,
        hands: List[HandInterface],
        trick_reference: TrickInterface):
        self.number_of_players = number_of_players
        self.trick_started_by = trick_started_by
        self.hands = hands
        self.trick_reference = trick_reference

    def _their_turn(self, player: int) -> bool:
        return player == (
        self.trick_started_by + self.trick_reference.size()
        ) % self.number_of_players

    def play(self, player: int, cardno: int) -> bool:
        if not self._their_turn(player):
            return False
        zahral = self.hands[player].play(cardno)
        if zahral and self.trick_reference.size() == self.number_of_players:
            self.trick_started_by = (
                    (
                    self.trick_started_by + self.trick_reference.winner()
                    ) % self.number_of_players
                )
            self.trick_reference.reset()
        return zahral

    def hand(self, player: int) -> List[str]:
        return [ card.string() for card in self.hands[player].cards() ]

    def trick(self) -> List[str]:
        return [ card.string() for card in self.trick_reference.cards() ]
