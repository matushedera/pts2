from typing import List, Optional

from .gameServerInterface import GameServerInterface
from .dealerInterface import DealerInterface
from .gameInterface import GameInterface

class GameServer(GameServerInterface):

    def __init__(self, dealer: DealerInterface):
        self.game: Optional[GameInterface] = None
        self.dealer: DealerInterface = dealer

    def play(self, player: int, cardno: int) -> bool:
        if self.game is None:
            return False
        return self.game.play(player, cardno)

    def new_game(self, number_of_players: int) -> bool:
        if not 1 < number_of_players < 5:
            return False
        if not self.game is None: # game in-progress won't be overwritten
            return False
        self.game = self.dealer.create_game(number_of_players)
        return True

    def hand(self, player: int) -> List[str]:
        if self.game is None:
            return []
        return self.game.hand(player)

    def trick(self) -> List[str]:
        if self.game is None:
            return []
        return self.game.trick()
