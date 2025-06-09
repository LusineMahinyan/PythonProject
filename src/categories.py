from collections import Counter
from typing import Dict, List


def count_by_categories(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.
    """
    counter = Counter()
    for tx in transactions:
        description = tx.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                counter[category] += 1
    return dict(counter)
