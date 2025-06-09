import re
from typing import Dict, List


def filter_by_description(transactions: List[Dict], keyword: str) -> List[Dict]:
    """
    Фильтрация операций по ключевому слову в описании с использованием регулярных выражений.
    """
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]


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
