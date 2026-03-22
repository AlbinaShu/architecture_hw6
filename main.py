import asyncio
from converters import UsdToRubConverter, UsdToEurConverter, UsdToGbpConverter, UsdToCnyConverter
from logger import setup_logging
from repositories import CurrencyRatesRepository

def main():    
    setup_logging()

    try:
        currency_amount = int(input('Введите значение в USD: \n'))
    except ValueError:
        print("Ошибка: введите число.")
        return

    currencyRatesRepository = CurrencyRatesRepository()

    converters = [
        UsdToRubConverter(currencyRatesRepository),
        UsdToEurConverter(currencyRatesRepository),
        UsdToGbpConverter(currencyRatesRepository),
        UsdToCnyConverter(currencyRatesRepository),
    ]

    for conv in converters:
        result = conv.convert(currency_amount)

if __name__ == "__main__":
    main()