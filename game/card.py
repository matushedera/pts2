from .cardInterface import CardInterface

class Card(CardInterface):

    def __init__(self, size_string: str):
        self.size_string: str = size_string

    def string(self) -> str:
        return self.size_string

    def _order_function(self, size_string: str) -> int:
        return [
            "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
        ].index(size_string)

    def is_ge(self, other: CardInterface) -> bool:
        if (self._order_function(self.size_string)
            >=
            self._order_function(other.size_string)
            ):
            return True
        return False
