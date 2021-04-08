from typing import List

class HandInterface:

    def play(self, cardno: int) -> bool:
        pass

    def cards(self) -> List[str]:
        pass

    def _is_lowest(self, cardno: int) -> bool:
        pass
