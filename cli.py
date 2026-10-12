from currency import (
    RatesError,
    convert,
    get_conversion_rates,
    load_rates,
    update_currency_rates,
)
from storage import format_cache_info

SHOW_TARGETS = ["RUB", "EUR", "GBP"]


def validate_currency_code(code: str, conversion_rates: dict) -> bool:
    code = code.upper()
    if not code:
        print("Код валюты не может быть пустым.")
        return False
    if code not in conversion_rates.keys():
        print(
            f"Код валюты «{code}» не найден. "
            "Доступные коды: см. пункт меню «Список валют»."
        )
        return False
    return True


def print_currency_list(currencies: list[str], columns: int = 10) -> None:
    for i in range(0, len(currencies), columns):
        print("  ".join(f"{c:5}" for c in currencies[i : i + columns]))


def show_base_rates(data: dict, base: str) -> None:
    base = base.upper()
    print(f"\nКурсы для 1 {base}:")
    for target in SHOW_TARGETS:
        if target == base:
            print(f"  {target}: 1 (та же валюта)")
            continue
        try:
            rate = convert(data, 1, base, target)
            print(f"  {target}: {rate:.6f}")
        except ValueError as exc:
            print(f"  {target}: недоступно ({exc})")
    print()


def run_cli() -> None:
    try:
        data = load_rates()
    except RatesError as exc:
        print(exc)
        return

    conversion_rates = get_conversion_rates(data)
    if not conversion_rates:
        print("В файле курсов нет данных о валютах.")
        return

    currencies = sorted(conversion_rates.keys())
    try:
        print(format_cache_info())
    except OSError:
        print("Не удалось прочитать дату обновления кэша.")
    print(f"Доступно валют: {len(currencies)}\n")

    while True:
        print("=" * 40)
        print("1 — Курсы базовой валюты (RUB, EUR, GBP)")
        print("2 — Конвертировать")
        print("3 — Список валют")
        print("4 — Обновить курсы сейчас")
        print("0 — Выход")
        choice = input("Выбор: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        if choice == "1":
            base = input("Базовая валюта (например USD): ").strip().upper()
            if not validate_currency_code(base, conversion_rates):
                continue
            show_base_rates(data, base)
            continue

        if choice == "3":
            print_currency_list(currencies)
            continue

        if choice == "4":
            try:
                data = update_currency_rates()
            except RatesError as exc:
                print(exc)
                continue
            conversion_rates = get_conversion_rates(data)
            currencies = sorted(conversion_rates.keys())
            try:
                print(format_cache_info())
            except OSError:
                print("Не удалось прочитать дату обновления кэша.")
            continue

        if choice != "2":
            print("Неизвестный пункт меню.")
            continue

        from_code = input("Из валюты (например USD): ").strip().upper()
        if not validate_currency_code(from_code, conversion_rates):
            continue

        to_code = input("В валюту (например RUB): ").strip().upper()
        if not validate_currency_code(to_code, conversion_rates):
            continue

        amount_raw = input("Сумма: ").strip().replace(",", ".")

        try:
            amount = float(amount_raw)
        except ValueError:
            print("Сумма должна быть числом.")
            continue

        if amount < 0:
            print("Сумма не может быть отрицательной.")
            continue

        try:
            result = convert(data, amount, from_code, to_code)
        except ValueError as exc:
            print(exc)
            continue

        print(f"\n{amount:g} {from_code} = {result:.4f} {to_code}\n")


if __name__ == "__main__":
    run_cli()
