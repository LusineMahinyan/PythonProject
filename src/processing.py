from datetime import datetime
from typing import Any, Dict, List

operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Функция, которая фильтрует список словарей по значению state"""
    result = []
    for operation in operations:
        if operation.get("state") == state:
            result.append(operation)
    return result


def sort_by_date(data: list[Dict[str, Any]], reverse: bool = True) -> list[Dict[str, Any]]:
    """Функция, которая сортирует список словарей по дате с валидацией"""

    def validate_and_parse_date(date_str: str) -> datetime:
        if not isinstance(date_str, str):
            raise TypeError(f"Expected string, got {type(date_str)}")
        if not date_str:
            raise ValueError("Date string cannot be empty")

        # Проверяем базовую структуру ISO формата
        if "T" not in date_str:
            raise ValueError(f"Invalid ISO date format: {date_str}")

        # Разбираем дату вручную
        date_part, time_part = date_str.split("T", 1)

        # Проверяем дату
        date_components = date_part.split("-")
        if len(date_components) != 3:
            raise ValueError(f"Invalid date format: {date_str}")

        year, month, day = date_components
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError(f"Invalid date format: {date_str}")

        # Проверяем время
        time_components = time_part.split(":")
        if len(time_components) < 3:
            raise ValueError(f"Invalid time format: {date_str}")

        hour, minute, second = time_components[:3]
        if not (hour.isdigit() and minute.isdigit()):
            raise ValueError(f"Invalid time format: {date_str}")

        # Проверяем секунды
        if "." in second:
            sec, micro = second.split(".", 1)
            if not (sec.isdigit() and micro.isdigit()):
                raise ValueError(f"Invalid time format: {date_str}")
        elif not second.isdigit():
            raise ValueError(f"Invalid time format: {date_str}")

        # Если все проверки пройдены, создаем datetime объект
        return datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            second=int(second.split(".")[0]),
            microsecond=int(second.split(".")[1]) if "." in second else 0,
        )

    return sorted(data, key=lambda x: validate_and_parse_date(x["date"]), reverse=reverse)
