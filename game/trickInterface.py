from typing import List

from .cardInterface import CardInterface

class TrickInterface:

    def play_as_lowest(self, c: CardInterface) -> bool:
        pass

    def play_normal(self, c: CardInterface) -> bool:
        pass

    def winner(self) -> int:
        pass

    def size(self) -> int:
        pass

    def cards(self) -> List[str]:
        pass

    def reset(self) -> None:
        pass
