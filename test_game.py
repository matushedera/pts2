import unittest
from typing import List

from game.gameServer import GameServer
from game.gameServerInterface import GameServerInterface
#from game.dealer import Dealer
from game.dealerInterface import DealerInterface
from game.game import Game
from game.card import Card
from game.cardInterface import CardInterface
from game.hand import Hand
from game.handInterface import HandInterface
#from game.trick import Trick
from game.trickInterface import TrickInterface

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

class HandSolitaryTestCase(unittest.TestCase):

    def setUp(self):
        class TrickMockTakeAny(TrickInterface):
            def play_as_lowest(self, c: CardInterface) -> bool:
                return True
            def play_normal(self, c: CardInterface) -> bool:
                return True
        class TrickMockTakeLowest(TrickInterface):
            def play_as_lowest(self, c: CardInterface) -> bool:
                return True
            def play_normal(self, c: CardInterface) -> bool:
                return False
        class TrickMockTakeNone(TrickInterface):
            def play_as_lowest(self, c: CardInterface) -> bool:
                return False
            def play_normal(self, c: CardInterface) -> bool:
                return False
        class CardMockLow(CardInterface):
            def is_ge(self, other) -> bool:
                if (other == self):
                    return True
                return False
        class CardMockHigh(CardInterface):
            def is_ge(self, other) -> bool:
                return True
        cards: List[CardInterface] = [
            CardMockHigh(),
            CardMockHigh(),
            CardMockHigh(),
            CardMockLow()
        ] # last one is lowest (no card is lower than itself)
        self.hand_trick_any: HandInterface = Hand(cards, TrickMockTakeAny())
        self.hand_trick_lowest: HandInterface = Hand(cards, TrickMockTakeLowest())
        self.hand_trick_none: HandInterface = Hand(cards, TrickMockTakeNone())

    def test_hand_all_cards_can_be_played(self):
        self.assertTrue(self.hand_trick_any.play(0))
        self.assertTrue(self.hand_trick_any.play(0)) # card with index 0 is popped
        self.assertTrue(self.hand_trick_any.play(0)) # each time it is possible to play it
        self.assertTrue(self.hand_trick_any.play(0))

    def test_hand_only_lowest_can_be_played(self):
        self.assertFalse(self.hand_trick_lowest.play(0))
        self.assertFalse(self.hand_trick_lowest.play(1))
        self.assertFalse(self.hand_trick_lowest.play(2))
        self.assertTrue(self.hand_trick_lowest.play(3))

    def test_hand_no_card_can_be_played(self):
        self.assertFalse(self.hand_trick_none.play(0))
        self.assertFalse(self.hand_trick_none.play(1))
        self.assertFalse(self.hand_trick_none.play(2))
        self.assertFalse(self.hand_trick_none.play(3))

    def test_hand_only_available_cards_can_be_played(self):
        self.assertFalse(self.hand_trick_any.play(-1))
        self.assertFalse(self.hand_trick_any.play(-9))
        self.assertFalse(self.hand_trick_any.play(5))
        self.assertFalse(self.hand_trick_any.play(10))
        self.assertTrue(self.hand_trick_any.play(3))
        self.assertTrue(self.hand_trick_any.play(2))
        self.assertTrue(self.hand_trick_any.play(1))
        self.assertTrue(self.hand_trick_any.play(0))

if __name__ == '__main__':
    unittest.main()
