import json
import os
import time
from datetime import datetime

CACHE_FILE = "currency_rate.json"
CACHE_MAX_AGE_HOURS = 24


def save_to_file(data: dict, path: str = CACHE_FILE) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_from_file(path: str = CACHE_FILE) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_cache_fresh(path: str = CACHE_FILE, max_age_hours: int = CACHE_MAX_AGE_HOURS) -> bool:
    if not os.path.exists(path):
        return False
    age_seconds = time.time() - os.path.getmtime(path)
    return age_seconds < max_age_hours * 3600


def format_cache_info(path: str = CACHE_FILE) -> str:
    mtime = os.path.getmtime(path)
    updated = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    return f"Кэш обновлён: {updated}"
