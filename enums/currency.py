from enum import Enum

class Currency(Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
    GBP = "GBP"
    CNY = "CNY"

    def __str__(self) -> str:
        return self.value