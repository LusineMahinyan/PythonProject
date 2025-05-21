from typing import Dict, Optional

import requests


def convert_to_rub(transaction: Dict[str, str]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли по текущему курсу.
    Принимает словарь транзакции с полями amount и currency.
    """
    try:
        amount = float(transaction["amount"])
        currency = transaction.get("currency", "RUB").upper()

        if currency == "RUB":
            return amount

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"

        headers = {"apikey": "M1LLZJPXXDuhFHdr4F48OF8kytXSxWfD"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        result = data.get("result")
        if result is None:
            return None

        return float(result)

    except (KeyError, ValueError, TypeError, requests.exceptions.RequestException) as e:
        print(f"Ошибка при конвертации валюты: {e}")
        return None


def get_transaction_amount_rub(transaction: Dict) -> Optional[float]:
    """Возвращает сумму транзакции в рублях."""
    return convert_to_rub(transaction)
