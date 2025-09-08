import re
from typing import List, Dict, Any


def filter_by_description(data: List[Dict[str, Any]], search_str: str) -> List[Dict[str, Any]]:
    """Фильтрует список операций по описанию с использованием регулярного выражения (поиск без учёта регистра)."""
    pattern = re.compile(search_str, re.IGNORECASE)
    return [item for item in data if "description" in item and pattern.search(item["description"])]


def filter_by_status(transactions: List[Dict], status: str) -> List[Dict]:
    """
    Фильтрация по статусу с учётом регистра.
    """
    return [tx for tx in transactions if tx.get("status", "").upper() == status.upper()]


def filter_by_currency(transactions: List[Dict], currency: str = "руб") -> List[Dict]:
    """
    Фильтрация по валюте (по подстроке в сумме).
    """
    return [tx for tx in transactions if currency.lower() in tx.get("amount", "").lower()]


def sort_by_date(transactions: List[Dict], ascending: bool = False) -> List[Dict]:
    """
    Сортировка по дате операций.
    """
    return sorted(transactions, key=lambda x: x.get("date", ""), reverse=not ascending)
