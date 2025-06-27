from collections import Counter
from typing import Dict, List


def count_by_categories(transactions: List[Dict[str, str]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.
    """
    counter: Counter[str] = Counter()
    for transaction in transactions:
        desc = transaction.get("description", "")
        for category in categories:
            if category.lower() in desc.lower():
                counter[category] += 1
    return dict(counter)
