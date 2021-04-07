import unittest

from game.gameServer import GameServer
from game.gameServerInterface import GameServerInterface
#from game.dealer import Dealer
from game.dealerInterface import DealerInterface
from game.game import Game
from game.card import Card
from game.cardInterface import CardInterface


class GameCreationTestCase(unittest.TestCase):

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

class CardTestCase(unittest.TestCase):

    def setUp(self):
        self.c8: CardInterface = Card("8")
        self.cJ: CardInterface = Card("J")
        self.cK: CardInterface = Card("K")
        self.cK2: CardInterface = Card("K")

    def test_card_sizes(self):
        self.assertTrue(self.c8.string() == "8")
        self.assertTrue(self.cJ.string() == "J")
        self.assertTrue(self.cK.string() == "K")
        self.assertTrue(self.cK2.string() == "K")

    def test_card_comparisson_resulting_in_false(self):
        self.assertFalse(self.c8.is_ge(self.cJ))
        self.assertFalse(self.c8.is_ge(self.cK))
        self.assertFalse(self.c8.is_ge(self.cK2))
        self.assertFalse(self.cJ.is_ge(self.cK))
        self.assertFalse(self.cJ.is_ge(self.cK2))

    def test_card_comparisson_resulting_in_true(self):
        self.assertTrue(self.cK2.is_ge(self.cK))
        self.assertTrue(self.cK2.is_ge(self.cJ))
        self.assertTrue(self.cK2.is_ge(self.c8))
        self.assertTrue(self.cK.is_ge(self.cK2))
        self.assertTrue(self.cK.is_ge(self.cJ))
        self.assertTrue(self.cK.is_ge(self.c8))
        self.assertTrue(self.cJ.is_ge(self.c8))


if __name__ == '__main__':
    unittest.main()
