import pytest
import time
from src.widgets import mask_account_card, get_date


@pytest.mark.parametrize("string, expected", [
    # Тесты для карт (16 цифр)
    ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),

    # Тесты для счетов (20 цифр)
    ("Счет 11112222333344445555", "Счет **5555"),
    ("Сберегательный счет 12345678901234567890", "Сберегательный счет **7890"),
])
def test_valid_masking(string, expected):
    assert mask_account_card(string) == expected


@pytest.mark.parametrize("string, expected", [
    # Неправильная длина
    ("Счет 1234567890123456789", "20 (для счета)"),  # 19 цифр
    ("Карта 123456789012345", "16 (для карты)"),  # 15 цифр

    # Недопустимые символы (буквы)
    ("Карта 1234-5678-9012-ABCD", "не содержит цифр"),
    ("Счет ABCDEFGHIJKLMNOPQRST", "не содержит цифр"),

    # Неполные данные
    ("1234567890123456", "Отсутствует название"),
    ("", "Передана пустая строка"),
])
def test_invalid_input(string, expected):
    with pytest.raises(ValueError):
        mask_account_card(string)


def test_performance_large_input():
    """Тест производительности на больших входных данных"""
    large_input = "Карта " + "1" * 10000  # 10000 цифр

    start_time = time.perf_counter()
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(large_input)
    execution_time = time.perf_counter() - start_time

    # Универсальная проверка для любого типа ошибки длины
    assert "цифр. Получено: 10000" in str(exc_info.value), (
        f"Неожиданное сообщение об ошибке: {str(exc_info.value)}"
    )
    assert execution_time < 0.1, (
        f"Слишком долгое выполнение: {execution_time:.4f} сек"
    )


@pytest.mark.parametrize("date_time, expected", [
    # Стандартные форматы дат
    ("2023-12-31T23:59:59", "31.12.2023"),
    ("2020-02-29T00:00:00", "29.02.2020"),  # Високосный год
    ("1999-01-01T12:00:00", "01.01.1999"),

    # Граничные случаи
    ("0001-01-01T00:00:00", "01.01.0001"),  # Минимальная дата
    ("9999-12-31T23:59:59", "31.12.9999"),  # Максимальная дата
    ("2023-01-09T00:00:00", "09.01.2023"),  # Однозначные день/месяц

    # Разные форматы времени
    ("2023-06-15T12:34:56.789", "15.06.2023"),
    ("2023-06-15T12:34:56+03:00", "15.06.2023"),
])
def test_valid_date_formats(date_time, expected):
    """Проверка корректного преобразования валидных дат"""
    assert get_date(date_time) == expected


@pytest.mark.parametrize("date_time, expected", [
    ("2023-12-31T23:59:59", "31.12.2023"),
    ("2020-02-29T00:00:00", "29.02.2020"),  # Високосный год
    ("1999-01-01T12:00:00", "01.01.1999"),
])
def test_valid_dates(date_time, expected):
    """Проверка корректного преобразования валидных дат"""
    assert get_date(date_time) == expected


@pytest.mark.parametrize("date_time, error_type, error", [
    # Неправильные форматы
    ("", ValueError, "Пустая строка"),
    ("2023-12-31", ValueError, "Неверный формат"),
    ("31.12.2023", ValueError, "Неверный формат"),
    ("2023/12/31T12:00:00", ValueError, "Неверный формат"),

    # Невалидные даты
    ("2023-AB-31T12:00:00", ValueError, "Неверный формат"),
    ("2023-13-01T00:00:00", ValueError, "Неверный формат"),
    ("2023-02-30T00:00:00", ValueError, "Неверный формат"),

    # Неправильные типы
    (None, TypeError, "Ожидается строка"),
    (1234567890, TypeError, "Ожидается строка"),
])
def test_invalid_inputs(date_time, error_type, error):
    """Проверка обработки некорректных входных данных"""
    with pytest.raises(error_type):
        get_date(date_time)



