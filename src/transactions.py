from typing import Dict, Optional
from src.external_api import convert_to_rub


def get_transaction_amount_rub(transaction: Dict) -> Optional[float]:
    """Возвращает сумму транзакции в рублях."""
    try:
        amount = float(transaction["amount"])
        currency = transaction.get("currency", "RUB").upper()

        if currency == "RUB":
            return amount

        return convert_to_rub(amount, currency)

    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка обработки транзакции: {e}")
        return None
