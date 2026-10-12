import requests

API_URL = "https://open.er-api.com/v6/latest/{base}"


def get_currency_rate(base: str) -> dict | None:
    url = API_URL.format(base=base)
    try:
        response = requests.get(url, timeout=15)
    except requests.Timeout:
        print(f"Ошибка сети: превышено время ожидания при запросе {base}.")
        return None
    except requests.ConnectionError:
        print(f"Ошибка сети: нет соединения при запросе {base}.")
        return None
    except requests.RequestException as exc:
        print(f"Ошибка сети при запросе {base}: {exc}")
        return None

    if response.status_code == 200:
        return response.json()
    print(f"Ошибка запроса {base}: сервер вернул код {response.status_code}.")
    return None
