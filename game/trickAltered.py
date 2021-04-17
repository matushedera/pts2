from typing import List

from .trick import Trick

class TrickAltered(Trick):

    def winner(self) -> int:
        winner = 0
        winner_card = self.table[0]
        for i in range(len(self.table)):
            if self.table[i].is_ge(winner_card) and (
                not winner_card.is_ge(self.table[i])
                #From equal cards, the player that played the equal card earliest wins the trick
            ):
                winner = i
                winner_card = self.table[i]
        return winner
