from typing import List

from .cardInterface import CardInterface

class HandInterface:

    def play(self, cardno: int) -> bool:
        pass

    def cards(self) -> List[CardInterface]:
        pass

    def _is_lowest(self, cardno: int) -> bool:
        pass
