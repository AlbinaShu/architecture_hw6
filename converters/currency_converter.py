import logging
from abc import ABC, abstractmethod
from typing import Optional

from interfaces import ICurrencyRatesRepository

class Converter(ABC):
    def __init__(self, rates_repository: ICurrencyRatesRepository) -> None:
        self._rates_repository = rates_repository
        self._logger = logging.getLogger(__name__)

    @abstractmethod
    def convert(self, amount: float) -> Optional[float]:
        pass