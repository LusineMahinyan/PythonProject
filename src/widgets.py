from typing import Union

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(string: Union[str, int]) -> str:
    """Функция кодировки счета/карты"""
    if string is None:
        raise ValueError("Не переданы входные данные")

    str_value = str(string).strip()
    if not str_value:
        raise ValueError("Передана пустая строка")

    parts = str_value.rsplit(maxsplit=1)
    if len(parts) < 2:
        if str_value.replace(" ", "").isdigit():
            raise ValueError("Отсутствует название карты/счета")
        raise ValueError("Неверный формат. Ожидается 'Название Номер'")

    name = parts[0]
    number_part = parts[1]

    cleaned_number = ""
    for symbol in number_part:
        if symbol.isdigit():
            cleaned_number += symbol

    if not cleaned_number:
        raise ValueError("Номер не содержит цифр")

    # Определяем тип по длине номера
    if len(cleaned_number) == 16:
        masked_number = get_mask_card_number(cleaned_number)
    elif len(cleaned_number) == 20:
        masked_number = get_mask_account(cleaned_number)
    else:
        card_digits = 16
        account_digits = 20

        if len(cleaned_number) < card_digits:
            required = f"{card_digits} (для карты)"
        else:
            required = f"{account_digits} (для счета)"
        raise ValueError(f"Номер должен содержать {required} цифр. " f"Получено: {len(cleaned_number)}")
    return f"{name} {masked_number}"


def get_date(date_time: str) -> str:
    """Функция для преобразования даты и времени в формат ДД.ММ.ГГГГ"""
    if not isinstance(date_time, str):
        raise TypeError("Ожидается строка с датой")

    if not date_time:
        raise ValueError("Пустая строка с датой")

    # Проверка формата (минимум 10 символов и правильные разделители)
    if len(date_time) < 10 or date_time[4] != "-" or date_time[7] != "-":
        raise ValueError("Неверный формат даты. Ожидается ГГГГ-ММ-ДДTHH:MM:SS")

    # Проверка наличия разделителя времени
    if "T" not in date_time:
        raise ValueError("Неверный формат даты. Отсутствует разделитель 'T'")

    # Извлечение компонентов даты
    year_part = date_time[:4]
    month_part = date_time[5:7]
    day_part = date_time[8:10]

    # Проверка, что компоненты являются числами
    if not (year_part.isdigit() and month_part.isdigit() and day_part.isdigit()):
        raise ValueError("Год, месяц и день должны быть числами")

    year = int(year_part)
    month = int(month_part)
    day = int(day_part)

    # Проверка валидности даты
    if month < 1 or month > 12:
        raise ValueError(f"Некорректный месяц: {month}")

    if day < 1 or day > 31:
        raise ValueError(f"Некорректный день: {day}")

    # Проверка количества дней в месяце
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    max_days = days_in_month[month - 1]

    # Проверка для февраля
    if month == 2 and (year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)):
        max_days = 29

    if day > max_days:
        raise ValueError(f"В {month} месяце нет {day} дня")

    return f"{day:02d}.{month:02d}.{year:04d}"
