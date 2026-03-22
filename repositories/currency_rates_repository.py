import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Dict, Optional

import requests

from enums import Currency
from interfaces import ICurrencyRatesRepository


@dataclass
class СurrencyRatesRepositoryConfig:
    api_url: str = "https://api.exchangerate-api.com/v4/latest/USD"
    cache_file: str = "exchange_rates.json"
    cache_expiry_seconds: int = 3600
    max_retries: int = 3
    retry_delay_seconds: int = 2
    timeout_seconds: int = 10


class CurrencyRatesRepository(ICurrencyRatesRepository):
    def __init__(self, config: Optional[СurrencyRatesRepositoryConfig] = None):
        self._config = config or СurrencyRatesRepositoryConfig()
        self._logger = logging.getLogger(__name__)
        self._rates: Optional[Dict[Currency, float]] = None

    def _load_from_cache(self) -> Optional[Dict[Currency, float]]:
        if not os.path.exists(self._config.cache_file):
            return None
        try:
            with open(self._config.cache_file, "r") as f:
                data = json.load(f)
                timestamp = data.get("timestamp")
                rates_data = data.get("rates")
                if timestamp and rates_data and (time.time() - timestamp) < self._config.cache_expiry_seconds:
                    rates = {}
                    for code, value in rates_data.items():
                        try:
                            rates[Currency(code)] = value
                        except ValueError:
                            self._logger.warning(f"Неизвестный код валюты: {code}")
                    self._logger.info("Загружены курсы из кэша")
                    return rates
        except (json.JSONDecodeError, KeyError, IOError) as e:
            self._logger.warning(f"Ошибка чтения кэша: {e}")
        return None

    def _save_to_cache(self, rates: Dict[Currency, float]) -> None:
        try:
            rates_data = {code.value: value for code, value in rates.items()}
            data = {"timestamp": time.time(), "rates": rates_data}
            with open(self._config.cache_file, "w") as f:
                json.dump(data, f)
            self._logger.info("Курсы сохранены в кэш")
        except IOError as e:
            self._logger.error(f"Ошибка сохранения кэша: {e}")

    def _fetch_from_api(self) -> Optional[Dict[Currency, float]]:
        for attempt in range(self._config.max_retries):
            try:
                response = requests.get(self._config.api_url, timeout=self._config.timeout_seconds)
                response.raise_for_status()
                data = response.json()
                rates_data = data.get("rates")
                if not rates_data:
                    self._logger.error("В ответе API отсутствует поле 'rates'")
                    return None
                rates = {}
                for code, value in rates_data.items():
                    try:
                        rates[Currency(code)] = value
                    except ValueError:
                        self._logger.warning(f"Неизвестный код валюты в API: {code}")
                self._logger.info("Курсы получены из API")
                return rates
            except requests.exceptions.RequestException as e:
                self._logger.error(
                    f"Запрос к API не удался (попытка {attempt + 1}/{self._config.max_retries}): {e}"
                )
                if attempt < self._config.max_retries - 1:
                    time.sleep(self._config.retry_delay_seconds)
            except (json.JSONDecodeError, KeyError) as e:
                self._logger.error(f"Ошибка обработки JSON: {e}")
                return None
        self._logger.error("Достигнуто максимальное число попыток, курсы не получены")
        return None

    def get_rates(self) -> Optional[Dict[Currency, float]]:
        if self._rates is None:
            self._rates = self._load_from_cache()
            if self._rates is None:
                self._rates = self._fetch_from_api()
                if self._rates:
                    self._save_to_cache(self._rates)
        return self._rates