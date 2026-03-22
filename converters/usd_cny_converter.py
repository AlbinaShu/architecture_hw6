from enums import Currency
from converters.currency_converter import Converter

class UsdToCnyConverter(Converter):
    def convert(self, amount: float) -> float | None:
        rates = self._rates_repository.get_rates()
        if rates is None:
            self._logger.error("Не удалось получить курсы валют.")
            return None

        rate = rates.get(Currency.CNY)

        converted_amount = amount * rate;

        print(f"{amount} USD to CNY: {converted_amount}")

        return converted_amount