
class GameServerInterface:

    def play(self, layer: int, cardno: int) -> bool:
        pass

    #def state(self, player: int) -> GameState:
        #pass

    def new_game(type: str) -> bool:
        pass
