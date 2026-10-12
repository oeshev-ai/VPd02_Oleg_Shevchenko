# Конвертер валют

Консольная программа для просмотра курсов и конвертации валют. Данные берутся из [Open Exchange Rate API](https://www.exchangerate-api.com/) и кэшируются локально на 24 часа.

## Возможности

- курсы базовой валюты к RUB, EUR, GBP
- конвертация любой доступной валюты в любую другую
- список кодов валют
- принудительное обновление курсов
- понятные сообщения при невалидном коде или ошибке сети

## Структура

| Файл | Назначение |
|------|------------|
| `api_client.py` | HTTP-запросы к API |
| `storage.py` | чтение/запись кэша |
| `currency.py` | загрузка, обновление, конвертация |
| `cli.py` | текстовый интерфейс |
| `currency_rate.json` | локальный кэш курсов (создаётся автоматически) |

## Установка

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

Linux / macOS:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python currency.py
```

или:

```bash
python cli.py
```

## Меню

1. Курсы базовой валюты (RUB, EUR, GBP)
2. Конвертировать
3. Список валют
4. Обновить курсы сейчас
0. Выход

## Примеры вывода

### 1 — Курсы базовой валюты

```text
Выбор: 1
Базовая валюта (например USD): usd

Курсы для 1 USD:
  RUB: 85.028588
  EUR: 0.892629
  GBP: 0.755605
```

### 2 — Конвертировать

```text
Выбор: 2
Из валюты (например USD): rub
В валюту (например RUB): gbp
Сумма: 100

100 RUB = 0.8885 GBP
```

### 3 — Список валют

```text
Выбор: 3
AED    AFN    ALL    AMD    ANG    AOA    ARS    AUD    AWG    AZN
BAM    BBD    BDT    BGN    BHD    BIF    BMD    BND    BOB    BRL
BSD    BTN    BWP    BYN    BZD    CAD    CDF    CHF    CLF    CLP
...
USD    UYU    UZS    VES    VND    VUV    WST    XAF    XCD    XCG
XDR    XOF    XPF    YER    ZAR    ZMW    ZWG    ZWL
```

## Кэш

Если файл `currency_rate.json` существует и моложе 24 часов, программа читает данные из него. Иначе запрашивает API и сохраняет результат.
