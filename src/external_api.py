import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv('.env')

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(amount: float, currency: str) -> Optional[float]:
    """Конвертирует сумму в рубли по текущему курсу."""
    if not API_KEY:
        raise ValueError("API key not configured. Check .env file")

    if currency == "RUB":
        return amount

    try:
        response = requests.get(
            BASE_URL,
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
            timeout=5
        )
        response.raise_for_status()
        rate = float(response.json()["rates"]["RUB"])
        return float(round(amount * rate, 2))

    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка конвертации: {e}")
        return None
