from masks import get_mask_account, get_mask_card_number


def mask_account_card(string: str) -> str:
    """Функция кодировки счета/карты"""
    parts = string.split()
    name = "".join(parts[:-1])
    number = parts[-1]
    number_int = int(number)
    masked_number_card = get_mask_card_number(number_int)
    masked_number_account = get_mask_account(number_int)
    if len(number) == 16:
        return f"{name} {masked_number_card}"
    elif len(number) == 20:
        return f"{name} {masked_number_account}"
    else:
        return "Ошибка: Номер некорректный."


print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card("MasterCard 7158300734726758"))
print(mask_account_card("Счет 35383033474447895560"))
print(mask_account_card("Visa Classic 6831982476737658"))
print(mask_account_card("Visa Platinum 8990922113665229"))
print(mask_account_card("Visa Gold 5999414228426353"))
print(mask_account_card("Счет 73654108430135874305"))


def get_date(date_time: str) -> str:
    """Функция для преобразования даты и времени в формат ДД.ММ.ГГГГ"""
    return f"{date_time[8:10]}.{date_time[5:7]}.{date_time[:4]}"


print(get_date("2024-03-11T02:26:18.671407"))
