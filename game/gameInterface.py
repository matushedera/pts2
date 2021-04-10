from typing import List

class GameInterface:

    def play(self, player: int, cardno: int) -> bool:
        pass

    def hand(self, player: int) -> List[str]:
        pass

    def trick(self) -> List[str]:
        pass
