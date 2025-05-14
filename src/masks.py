from typing import Union

def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Функция маскировки номера банковской карты
    :rtype: object
    """
    card_number_str = str(card_number).strip()
    digits = card_number_str.replace(" ", "").replace("-", "")

    if not digits.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(digits) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"


def get_mask_account(account_number: Union[int, str]) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску"""
    account_number_str = str(account_number).strip()
    digits_1 = account_number_str.replace(" ", "").replace("-", "")

    if not digits_1.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")
    if len(digits_1) != 20:
        raise ValueError("Номер счёта должен содержать 20 цифр")

    return "**" + digits_1[-4:]
