from .game import Game

class DealerInterface:

    def create_game(self, number_of_players: int) -> Game:
        pass
