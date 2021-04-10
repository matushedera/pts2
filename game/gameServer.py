from typing import List

from .gameServerInterface import GameServerInterface
from .dealerInterface import DealerInterface

class GameServer(GameServerInterface):

    def __init__(self, dealer: DealerInterface):
        self.game = None
        self.dealer = dealer

    def play(self, player: int, cardno: int) -> bool:
        return self.game.play(player, cardno)

    def new_game(self, number_of_players: int) -> bool:
        if not 1 < number_of_players < 5:
            return False
        if self.game != None: # game in-progress won't be overwritten
            return False
        self.game = self.dealer.create_game(number_of_players)
        return True

    def hand(self, player: int) -> List[str]:
        return self.game.hand(player)

    def trick(self) -> List[str]:
        return self.game.trick()
