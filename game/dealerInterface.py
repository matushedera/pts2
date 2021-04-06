from .game import Game

class DealerInterface:

    def create_game(type: str) -> Game:
        pass
