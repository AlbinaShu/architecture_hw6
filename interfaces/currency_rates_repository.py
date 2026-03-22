from abc import ABC, abstractmethod
from typing import Dict, Optional

from enums import Currency

class ICurrencyRatesRepository(ABC):
    @abstractmethod
    def get_rates(self) -> Optional[Dict[Currency, float]]:
        pass