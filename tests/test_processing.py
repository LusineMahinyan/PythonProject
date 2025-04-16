import pytest

from src.processing import filter_by_state, operations, sort_by_date


@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("CANCELED", 2),
    ("PENDING", 0),  # тест для несуществующего статуса
])
def test_filter_by_state(state: str, expected_count: int) -> None:
    """Тестирование фильтрации операций по статусу"""
    filtered_ops = filter_by_state(operations, state)
    assert len(filtered_ops) == expected_count
    for op in filtered_ops:
        assert op["state"] == state


def test_filter_by_state_default() -> None:
    """Тестирование фильтрации с параметром state по умолчанию (EXECUTED)"""
    filtered_ops = filter_by_state(operations)
    assert len(filtered_ops) == 2
    for op in filtered_ops:
        assert op["state"] == "EXECUTED"


def test_filter_by_state_empty_input() -> None:
    """Тестирование функции с пустым списком операций"""
    assert filter_by_state([], "EXECUTED") == []


test_data = [
    {"date": "2023-01-15T12:00:00.000000", "id": 1},
    {"date": "2022-05-20T08:30:00.000000", "id": 2},
    {"date": "2023-01-15T12:00:00.000000", "id": 3},
    {"date": "2021-12-31T23:59:59.999999", "id": 4},
]


@pytest.mark.parametrize("reverse, expected_order", [
    (True, [1, 3, 2, 4]),  # Сортировка по убыванию (новые сначала)
    (False, [4, 2, 1, 3]),  # Сортировка по возрастанию (старые сначала)
])
def test_sort_by_date_direction(
        reverse: bool,
        expected_order: list[int]
) -> None:
    """Тестирование сортировки по дате в разных направлениях"""
    sorted_data = sort_by_date(test_data, reverse=reverse)
    assert [item["id"] for item in sorted_data] == expected_order


def test_sort_by_date_stable_sort() -> None:
    """Тестирование стабильности сортировки при одинаковых датах"""
    sorted_data = sort_by_date(test_data, reverse=True)
    # Проверяем что при одинаковых датах порядок элементов сохраняется
    assert sorted_data[0]["id"] == 1
    assert sorted_data[1]["id"] == 3


def test_sort_by_date_empty_input() -> None:
    """Тестирование функции с пустым списком"""
    assert sort_by_date([]) == []


def test_sort_by_date_single_item() -> None:
    """Тестирование функции с одним элементом"""
    single_item = [{"date": "2023-01-01T00:00:00.000000", "id": 1}]
    assert sort_by_date(single_item) == single_item


@pytest.mark.parametrize("invalid_date", [
    "invalid-date-format",  # Неправильный формат даты
    "2023/01/01 12:00:00",  # Нестандартный формат
    "",  # Пустая строка
    None,  # None вместо даты
])
def test_sort_by_date_invalid_formats(invalid_date: str) -> None:
    """Тестирование обработки некорректных форматов дат"""
    test_data_with_invalid = [
        {"date": "2023-01-01T00:00:00.000000", "id": 1},
        {"date": invalid_date, "id": 2},
        {"date": "2022-01-01T00:00:00.000000", "id": 3},
    ]
    if invalid_date is None:
        with pytest.raises(TypeError):
            sort_by_date(test_data_with_invalid)
    elif invalid_date == "":
        with pytest.raises(ValueError):
            sort_by_date(test_data_with_invalid)
    else:
        with pytest.raises(ValueError):
            sort_by_date(test_data_with_invalid)
