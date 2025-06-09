from typing import Any, Dict, List


def format_transaction(tx: Dict) -> str:
    return f"""{tx.get('date')} {tx.get('description')}
{tx.get('from', '')} -> {tx.get('to', '')}
Сумма: {tx.get('amount')}"""


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for tx in transactions:
        print(format_transaction(tx))
        print()
