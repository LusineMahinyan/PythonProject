from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions_1() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Transaction 1",
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "EUR"}},
            "description": "Transaction 2",
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Transaction 3",
        },
        {
            "id": 4,
            "operationAmount": {"currency": {"code": "GBP"}},
            "description": "Transaction 4",
        },
    ]


def test_filters_usd_transactions(
        sample_transactions_1: List[Dict[str, Any]]
) \
        -> None:
    """Проверяет, что функция корректно фильтрует USD-транзакции."""
    usd_transactions = list(filter_by_currency(sample_transactions_1, "USD"))
    assert len(usd_transactions) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD"
               for t in usd_transactions)
    assert {t["id"] for t in usd_transactions} == {1, 3}


def test_filters_eur_transactions(
        sample_transactions_1: List[Dict[str, Any]]
) \
        -> None:
    """Проверяет, что функция корректно фильтрует EUR-транзакции."""
    eur_transactions = list(filter_by_currency(sample_transactions_1, "EUR"))
    assert len(eur_transactions) == 1
    assert eur_transactions[0]["id"] == 2


def test_no_matching_currency(
        sample_transactions_1: List[Dict[str, Any]]
) \
        -> None:
    """Проверяет, что возвращается пустой список,
    если нет подходящих транзакций."""
    jpy_transactions = list(filter_by_currency(sample_transactions_1, "JPY"))
    assert not jpy_transactions


def test_empty_transactions_list() -> None:
    """Проверяет, что функция корректно
    обрабатывает пустой список транзакций."""
    empty_transactions: List[Dict[str, Any]] = []
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert not result  # Должен вернуться пустой генератор


def test_transactions_missing_currency_field() \
        -> None:
    """Проверяет, что функция не падает,
    если у транзакции нет поля 'currency'."""
    broken_transactions = [
        {"id": 1, "operationAmount": {"amount": 100}},  # Нет currency
        {"id": 2,
         "operationAmount": {"currency": {"code": "USD"}}},  # Корректная
    ]
    usd_transactions = list(filter_by_currency(broken_transactions, "USD"))
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["id"] == 2


@pytest.fixture
def sample_transactions() -> List[Dict]:
    return [
        {"description": "Оплата услуг",
         "id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"description": "Перевод другу",
         "id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"description": "Покупка в магазине",
         "id": 3, "operationAmount": {"currency": {"code": "USD"}}},
    ]


def test_returns_correct_descriptions(sample_transactions: List[Dict]) -> None:
    """Проверяет корректное извлечение описаний транзакций."""
    descriptions = list(transaction_descriptions(sample_transactions))

    # Проверка количества элементов (теперь ожидаем 3)
    assert len(descriptions) == 3

    # Проверка конкретных значений
    assert descriptions == [
        "Оплата услуг",
        "Перевод другу",
        "Покупка в магазине",
    ]


def test_yields_descriptions_one_by_one(
        sample_transactions: List[Dict]
)\
        -> None:
    """Проверяет, что функция возвращает описания по одному (генератор)."""
    generator = transaction_descriptions(sample_transactions)

    # Проверяем тип объекта
    from collections.abc import Iterator

    assert isinstance(generator, Iterator)

    # Проверяем фактические значения из фикстуры
    assert next(generator) == "Оплата услуг"
    assert next(generator) == "Перевод другу"
    assert next(generator) == "Покупка в магазине"

    # Проверяем завершение генератора
    with pytest.raises(StopIteration):
        next(generator)


def test_empty_transactions_list_1() -> None:
    """Проверяет работу с пустым списком транзакций."""
    empty_transactions: List[Dict] = []
    descriptions = list(transaction_descriptions(empty_transactions))
    assert descriptions == []


def test_transaction_without_description() -> None:
    """Проверяет обработку транзакции без поля 'description'."""
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "description": "Оплата услуг"},
        {"id": 2},  # Транзакция без описания
        {"id": 3, "description": "Покупка"},
    ]

    with pytest.raises(KeyError):
        list(transaction_descriptions(transactions))


def test_generates_correct_range() -> None:
    """Проверяет генерацию номеров в заданном диапазоне."""
    generator = card_number_generator(1, 3)
    numbers = list(generator)

    assert numbers == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]


def test_card_number_formatting() -> None:
    """Проверяет корректность форматирования номеров."""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    number = next(generator)

    assert number == "1234 5678 9012 3456"
    assert len(number) == 19  # 16 цифр + 3 пробела
    assert number.count(" ") == 3


def test_single_value_range() -> None:
    """Проверяет обработку диапазона из одного элемента."""
    generator = card_number_generator(9999999999999999, 9999999999999999)
    numbers = list(generator)

    assert numbers == ["9999 9999 9999 9999"]
    assert len(numbers) == 1


def test_empty_range() -> None:
    """Проверяет обработку пустого диапазона (start > end)."""
    generator = card_number_generator(10, 5)
    numbers = list(generator)

    assert numbers == []


def test_generator_stops_correctly() -> None:
    """Проверяет корректное завершение генератора."""
    generator = card_number_generator(1, 1)

    assert next(generator) == "0000 0000 0000 0001"

    with pytest.raises(StopIteration):
        next(generator)  # Генератор должен завершиться


def test_large_numbers() -> None:
    """Проверяет генерацию больших номеров карт."""
    generator = card_number_generator(9999999999999990, 9999999999999999)
    numbers = list(generator)

    assert len(numbers) == 10
    assert numbers[0] == "9999 9999 9999 9990"
    assert numbers[-1] == "9999 9999 9999 9999"
