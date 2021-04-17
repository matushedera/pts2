from .card import Card
from .cardInterface import CardInterface

class CardAltered(Card):

    def is_ge(self, other: CardInterface) -> bool:
        if self.string() >= other.string():
            return True
        return False
