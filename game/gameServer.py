from .gameServerInterface import GameServerInterface
from .dealerInterface import DealerInterface

class GameServer(GameServerInterface):

    def __init__(self, dealer: DealerInterface):
        self.game = None
        self.dealer = dealer

    def new_game(self, number_of_players: int) -> bool:
        if not 1 < number_of_players < 5:
            return False
        if self.game != None: # game in-progress won't be overwritten
            return False
        self.game = self.dealer.create_game(number_of_players)
        return True
