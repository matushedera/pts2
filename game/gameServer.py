from .gameServerInterface import GameServerInterface
from .dealerInterface import DealerInterface

class GameServer(GameServerInterface):

    def __init__(self, dealer: DealerInterface):
        self.game = None
        self.dealer = dealer

    def new_game(self, type: int) -> bool:
        if self.game != None: # game in-progress won't be overwritten
            return False
        self.game = self.dealer.create_game()
        return True
