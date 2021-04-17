from typing import List

from .handInterface import HandInterface
from .trickInterface import TrickInterface
from .cardInterface import CardInterface

class Hand(HandInterface):

    def __init__(self, cards: List[CardInterface], trick: TrickInterface):
        self.card_list: List[CardInterface] = cards
        self.trick: TrickInterface = trick

    def play(self, cardno: int) -> bool:
        if not 0 <= cardno < len(self.card_list):
            return False
        if self.trick.play_normal(self.card_list[cardno]):
            self.card_list.pop(cardno)
            return True
        if self._is_lowest(cardno) and self.trick.play_as_lowest(self.card_list[cardno]):
            self.card_list.pop(cardno)
            return True
        return False

    def cards(self) -> List[CardInterface]:
        return self.card_list

    def _is_lowest(self, cardno: int) -> bool:
        for other in self.card_list:
            if not other.is_ge(self.card_list[cardno]): # some card is lower
                return False
        return True
