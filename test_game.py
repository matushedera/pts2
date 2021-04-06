import unittest

from game.gameServer import GameServer
from game.gameServerInterface import GameServerInterface
#from dealer import Dealer
from game.dealerInterface import DealerInterface
from game.game import Game

class ServerSolitary(unittest.TestCase):

    def test_creating__games(self):
        class DealerMock(DealerInterface):
            def create_game(type: int) -> Game:
                return Game()
        di: DealerInterface = DealerMock()
        gsi: GameServerInterface = GameServer(di)
        self.assertTrue(gsi.new_game(3)) # initial initialization is possible
        self.assertFalse(gsi.new_game(2)) # subsequent initialization is impossible

if __name__ == '__main__':
    unittest.main()
