import unittest

from game.gameServer import GameServer
from game.gameServerInterface import GameServerInterface
#from dealer import Dealer
from game.dealerInterface import DealerInterface
from game.game import Game

class ServerDealerGame(unittest.TestCase):

    def setUp(self):
        class DealerMock(DealerInterface):
            def create_game(self, number_of_players: int) -> Game:
                return Game(number_of_players, 0)
        di: DealerInterface = DealerMock()
        self.gsi: GameServerInterface = GameServer(di)

    def test_creating_multiple_games(self):
        self.assertTrue(self.gsi.new_game(3)) # initial initialization is possible
        self.assertFalse(self.gsi.new_game(2)) # subsequent initialization is impossible

    def test_creating_game_for_1_and_2_players(self):
        self.assertFalse(self.gsi.new_game(1), "game is for 2-4 players only")
        self.assertTrue(self.gsi.new_game(2), "game doesn't initialize for 2 players")
        self.assertEqual(self.gsi.game.number_of_players, 2)

    def test_creating_game_for_4_and_5_players(self):
        self.assertFalse(self.gsi.new_game(5), "game is for 2-4 players only")
        self.assertTrue(self.gsi.new_game(4), "game doesn't initialize for 4 players")
        self.assertEqual(self.gsi.game.number_of_players, 4)

    def test_initial_trick_starting_player(self):
        self.gsi.new_game(3)
        self.assertEqual(self.gsi.game.trick_started_by, 0, "player 0 should start initial trick")


if __name__ == '__main__':
    unittest.main()
