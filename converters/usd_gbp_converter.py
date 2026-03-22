from enums import Currency
from converters.currency_converter import Converter

class UsdToGbpConverter(Converter):
    def convert(self, amount: float) -> float | None:
        rates = self._rates_repository.get_rates()
        if rates is None:
            self._logger.error("Не удалось получить курсы валют.")
            return None

        rate = rates.get(Currency.GBP)

        converted_amount = amount * rate;

        print(f"{amount} USD to GBR: {converted_amount}")

        return converted_amount