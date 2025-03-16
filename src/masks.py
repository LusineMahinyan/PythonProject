def get_mask_card_number(card_number: int) -> str:
    """Функция маскировки номера банковской карты"""
    card_number_str = str(card_number)
    return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"


print(get_mask_card_number(7000792289606361))


def get_mask_account(account_number: int) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску"""
    account_number_str = str(account_number)
    return "**" + account_number_str[-4:]


print(get_mask_account(73654108430135874305))