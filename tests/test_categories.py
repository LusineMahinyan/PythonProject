from typing import Dict, List

import pytest

from src.categories import count_by_categories  # исправлен импорт


@pytest.fixture
def transactions_sample() -> List[Dict[str, str]]:
    return [
        {"description": "Оплата интернета", "amount": "1200 руб."},
        {"description": "Перевод в другой банк", "amount": "5000 руб."},
        {"description": "Покупка в магазине", "amount": "3500 руб."},
        {"description": "Оплата мобильной связи", "amount": "800 руб."},
        {"description": "Перевод другу", "amount": "1000 руб."},
        {"description": "Покупка билетов", "amount": "2500 руб."},
    ]


def test_count_by_single_category(transactions_sample: List[Dict[str, str]]) -> None:
    categories = ["оплата"]
    result = count_by_categories(transactions_sample, categories)
    assert result == {"оплата": 2}


def test_count_by_multiple_categories(transactions_sample: List[Dict[str, str]]) -> None:
    categories = ["оплата", "перевод", "покупка"]
    result = count_by_categories(transactions_sample, categories)
    assert result == {"оплата": 2, "перевод": 2, "покупка": 2}


def test_count_with_no_matches(transactions_sample: List[Dict[str, str]]) -> None:
    categories = ["налог", "штраф"]
    result = count_by_categories(transactions_sample, categories)
    assert result == {}


def test_count_is_case_insensitive() -> None:
    transactions: List[Dict[str, str]] = [
        {"description": "ПЕРЕВОД в банк"},
        {"description": "перевод на карту"},
        {"description": "Перевод другу"},
    ]
    categories = ["перевод"]
    result = count_by_categories(transactions, categories)
    assert result == {"перевод": 3}


def test_count_skips_missing_description() -> None:
    transactions: List[Dict[str, str]] = [
        {"description": "Оплата"},
        {"amount": "1000 руб."},  # отсутствует описание
    ]
    result = count_by_categories(transactions, ["оплата"])
    assert result == {"оплата": 1}
