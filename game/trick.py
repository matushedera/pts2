from typing import List

from .trickInterface import TrickInterface
from .cardInterface import CardInterface

class Trick(TrickInterface):

    def __init__(self):
        self.table: List[CardInterface] = []

    def play_as_lowest(self, c: CardInterface) -> bool:
        self.table.append(c)
        return True

    def play_normal(self, c: CardInterface) -> bool:
        for previous in self.table:
            if not c.is_ge(previous):
                return False
        self.table.append(c)
        return True

    def winner(self) -> int:
        winner = 0
        winner_card = self.table[0]
        for i in range(len(self.table)):
            if self.table[i].is_ge(winner_card):
                winner = i
                winner_card = self.table[i]
        return winner


    def size(self) -> int:
        return len(self.table)

    def cards(self) -> List[CardInterface]:
        return self.table

    def reset(self) -> None:
        self.table = []
