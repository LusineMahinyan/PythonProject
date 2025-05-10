from typing import Optional
import requests


def convert_to_rub(amount: float, currency: str) -> Optional[float]:
    """Конвертирует сумму в рубли по текущему курсу."""
    if currency == "RUB":
        return amount

    try:
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/latest",
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": "ваш_api_ключ"},
            timeout=5
        )
        response.raise_for_status()

        rate = float(response.json()["rates"]["RUB"])
        result = amount * rate
        return float(round(result, 2))

    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка конвертации: {e}")
        return None
