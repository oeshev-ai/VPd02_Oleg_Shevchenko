from api_client import get_currency_rate
from storage import (
    CACHE_FILE,
    is_cache_fresh,
    read_from_file,
    save_to_file,
)
import os

FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]


class RatesError(Exception):
    """Ошибка загрузки или обновления курсов (для понятного вывода в CLI)."""


def update_currency_rates() -> dict:
    all_data = {}
    for currency in FAVORITE_CURRENCIES:
        print(f"Загрузка курсов для {currency}...")
        rate = get_currency_rate(currency)
        if rate is None:
            raise RatesError(
                f"Не удалось получить курсы для {currency}. "
                "Проверьте интернет-соединение и попробуйте позже."
            )
        all_data[currency] = rate
    save_to_file(all_data)
    print(f"Данные обновлены в {CACHE_FILE}")
    return all_data


def load_rates() -> dict:
    if is_cache_fresh():
        print("Используем локальный файл (младше 24 часов).")
        return read_from_file()

    print("Файл отсутствует или старше 24 часов — обновляем...")
    try:
        return update_currency_rates()
    except RatesError as exc:
        if os.path.exists(CACHE_FILE):
            print(f"{exc}")
            print("Используем устаревший локальный файл.")
            return read_from_file()
        raise RatesError(
            f"{exc} Локальный файл курсов тоже отсутствует — работа невозможна."
        ) from None


def get_conversion_rates(data: dict) -> dict:
    """Словарь курсов: код валюты → курс (из первого доступного блока rates)."""
    for base_data in data.values():
        rates = base_data.get("rates")
        if rates:
            return rates
    return {}


def available_currencies(data: dict) -> list[str]:
    conversion_rates = get_conversion_rates(data)
    return sorted(conversion_rates.keys())


def convert(data: dict, amount: float, from_code: str, to_code: str) -> float:
    from_code = from_code.upper()
    to_code = to_code.upper()
    conversion_rates = get_conversion_rates(data)

    if from_code not in conversion_rates.keys():
        raise ValueError(f"Код валюты «{from_code}» не найден.")
    if to_code not in conversion_rates.keys():
        raise ValueError(f"Код валюты «{to_code}» не найден.")

    if from_code == to_code:
        return amount

    if from_code in data:
        rates = data[from_code].get("rates", {})
        return amount * rates[to_code]

    return amount * (conversion_rates[to_code] / conversion_rates[from_code])


if __name__ == "__main__":
    from cli import run_cli

    run_cli()
