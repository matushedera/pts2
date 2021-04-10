from typing import List

class GameServerInterface:

    def play(self, player: int, cardno: int) -> bool:
        pass

    def new_game(type: str) -> bool:
        pass

    def hand(self, player: int) -> List[str]:
        pass

    def trick(self) -> List[str]:
        pass
