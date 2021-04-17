import unittest
from typing import List

from game.gameServer import GameServer
from game.gameServerInterface import GameServerInterface
from game.dealer import Dealer
from game.dealerInterface import DealerInterface
from game.game import Game
from game.card import Card
from game.cardInterface import CardInterface
from game.hand import Hand
from game.handInterface import HandInterface
from game.trick import Trick
from game.trickInterface import TrickInterface
from game.trickAltered import TrickAltered

class GameCreationTestCase(unittest.TestCase):

    def setUp(self):
        class DealerMock(DealerInterface):
            def create_game(self, number_of_players: int) -> Game:
                return Game(number_of_players, 0, [], Trick())
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

class GamePlayTestCase(unittest.TestCase):

    def setUp(self):
        class DealerMock(DealerInterface):
            def create_game(self, number_of_players: int) -> Game:
                pass
        trick: TrickInterface = Trick()
        hand1: HandInterface = (
            Hand([Card("2"), Card("6"), Card("7"), Card("A"), Card("Q"), Card("4")], trick)
        )
        hand2: HandInterface = (
            Hand([Card("A"), Card("A"), Card("J"), Card("5"), Card("8"), Card("K")], trick)
        )
        hand3: HandInterface = (
            Hand([Card("J"), Card("3"), Card("9"), Card("10"), Card("J"), Card("3")], trick)
        )
        self.game_server: GameServerInterface = GameServer(DealerMock())
        self.game_server.game = Game(3, 0, [hand1, hand2, hand3], trick)

        trick_altered: TrickInterface = TrickAltered();
        hand1: HandInterface = (
            Hand([Card("2"), Card("6"), Card("7"), Card("A"), Card("Q"), Card("4")], trick_altered)
        )
        hand2: HandInterface = (
            Hand([Card("A"), Card("A"), Card("J"), Card("5"), Card("8"), Card("K")], trick_altered)
        )
        hand3: HandInterface = (
            Hand([Card("J"), Card("3"), Card("9"), Card("10"), Card("J"), Card("3")], trick_altered)
        )
        self.game_server_altered: GameServerInterface = GameServer(DealerMock())
        self.game_server_altered.game = Game(3, 0, [hand1, hand2, hand3], trick_altered)

    def test_gameplay_initial_hands(self):
        self.assertEqual(self.game_server.hand(0), ["2", "6", "7", "A", "Q", "4"])
        self.assertEqual(self.game_server.hand(1), ["A", "A", "J", "5", "8", "K"])
        self.assertEqual(self.game_server.hand(2), ["J", "3", "9", "10", "J", "3"])

    def test_gameplay_turns(self): #(player 2 played greater/equal card last)
        self.assertFalse(self.game_server.play(1, 2), "it's player's 0 turn")
        self.assertTrue(self.game_server.play(0, 2), "it's player's 0 turn") # player 0 played "7"
        self.assertTrue(self.game_server.play(1, 2), "it's player's 1 turn") # player 1 played "J"
        self.assertFalse(self.game_server.play(1, 4), "it's player's 2 turn")
        self.assertFalse(self.game_server.play(0, 5), "it's player's 2 turn")
        self.assertTrue(self.game_server.play(2, 0), "it's player's 2 turn") # player 2 played "J"
        self.assertTrue(self.game_server.play(2, 0), "it's player's 2 turn, because he won previous trick")

    def test_altered_gameplay_turns(self): #(player 2 played greater/equal card earliest)
        self.assertFalse(self.game_server_altered.play(1, 2), "it's player's 0 turn")
        self.assertTrue(self.game_server_altered.play(0, 2), "it's player's 0 turn") # player 0 played "7"
        self.assertTrue(self.game_server_altered.play(1, 2), "it's player's 1 turn") # player 1 played "J"
        self.assertFalse(self.game_server_altered.play(1, 4), "it's player's 2 turn")
        self.assertFalse(self.game_server_altered.play(0, 5), "it's player's 2 turn")
        self.assertTrue(self.game_server_altered.play(2, 0), "it's player's 2 turn") # player 2 played "J"
        self.assertTrue(self.game_server_altered.play(1, 0), "it's player's 1 turn, because he won previous trick")

    def test_gameplay_greater_or_equal_or_his_lowest(self):
        self.assertTrue(self.game_server.play(0, 4), "table is empty") # player 0 played "Q"
        self.assertFalse(self.game_server.play(1, 4), "8 isn't his lowest and is not GE") # player 1 played "8"
        self.assertTrue(self.game_server.play(1, 1), "A is GE") # player 1 played "A"
        self.assertFalse(self.game_server.play(2, 3), "10 isn't his lowest and is not GE") # player 2 played "10"
        self.assertTrue(self.game_server.play(2, 1), "3 in not GE but it is his lowest") # player 2 played "3"

    def test_gameplay_tricks_and_hands(self):
        self.game_server.play(0, 2) # player 0 played "7"
        self.assertEqual(self.game_server.hand(0), ["2", "6", "A", "Q", "4"]) # "7 is missing"
        self.game_server.play(1, 2) # player 1 played "J"
        self.assertEqual(self.game_server.hand(1), ["A", "A", "5", "8", "K"]) # "J" is missing
        self.assertEqual(self.game_server.trick(), ["7", "J"]) # played cards are on the table
        self.game_server.play(2, 0) # player 2 played "J"
        self.assertEqual(self.game_server.hand(2), ["3", "9", "10", "J", "3"]) # "J" is missing
        self.assertEqual(self.game_server.trick(), []) # table is empty because new trick started'
        self.game_server.play(2, 0) # player 2 played "3" (it's his turn because he won previous trick)
        self.assertEqual(self.game_server.hand(2), ["9", "10", "J", "3"]) # "3" is missing
        self.game_server.play(0, 3) # player 0 played "Q"
        self.assertEqual(self.game_server.hand(0), ["2", "6", "A", "4"]) # "Q is missing"
        self.assertEqual(self.game_server.trick(), ["3", "Q"]) # played cards are on the table
        self.game_server.play(1, 4) # player 1 played "K"
        self.assertEqual(self.game_server.hand(1), ["A", "A", "5", "8"]) # "K" is missing
        self.assertEqual(self.game_server.trick(), []) # table is empty because new trick started'
        self.game_server.play(1, 1) # player 1 played "A" (it's his turn because he won previous trick)
        self.assertEqual(self.game_server.hand(1), ["A", "5", "8"]) # "A" is missing
        self.assertEqual(self.game_server.trick(), ["A"]) # played cards are on the table
        self.game_server.play(2, 3) # player 2 played "3" (his lowest)
        self.assertEqual(self.game_server.hand(2), ["9", "10", "J"]) # "3" is missing
        self.game_server.play(0, 0) # player 0 played "2" (his lowest)
        self.assertEqual(self.game_server.hand(0), ["6", "A", "4"]) # "2 is missing"
        self.game_server.play(1, 1)
        self.assertEqual(self.game_server.hand(1), ["A", "8"])
        self.game_server.play(2, 2)
        self.assertEqual(self.game_server.hand(2), ["9", "10"])
        self.game_server.play(0, 2)
        self.assertEqual(self.game_server.hand(0), ["6", "A"])
        self.game_server.play(2, 1)
        self.assertEqual(self.game_server.hand(2), ["9"])
        self.game_server.play(0, 1)
        self.assertEqual(self.game_server.hand(0), ["6"]) # lowest remaining card
        self.game_server.play(1, 1)
        self.assertEqual(self.game_server.hand(1), ["A"])





if __name__ == '__main__':
    unittest.main()
