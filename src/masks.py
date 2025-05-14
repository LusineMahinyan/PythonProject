import logging
from typing import Union

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/masks.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Функция маскировки номера банковской карты"""
    logging.debug("Начало маскировки номера банковской карты.")
    try:
        card_number_str = str(card_number).strip()
        digits = card_number_str.replace(" ", "").replace("-", "")

        logger.debug(f"Обработка номера карты {card_number_str}")
        if not digits.isdigit():
            logger.error("Номер карты содержит недопустимые символы.")
            raise ValueError("Номер карты должен содержать только цифры.")

        if len(digits) != 16:
            logger.error(f"Некорректная длина номера карты {len(digits)}")
            raise ValueError("Номер карты должен содержать 16 цифр.")

        mask_card_number = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
        logger.info("Успешно замаскирован номер карты.")
        return mask_card_number

    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера карты {e}.")
        raise


def get_mask_account(account_number: Union[int, str]) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску"""
    logger.debug("Начало маскировки номера счета")
    try:
        account_number_str = str(account_number).strip()
        digits_1 = account_number_str.replace(" ", "").replace("-", "")

        logger.debug(f"Обработка номера счета {account_number_str}")
        if not digits_1.isdigit():
            logger.error("Номер счета содержит недопустимые символы.")
            raise ValueError("Номер счёта должен содержать только цифры.")

        if len(digits_1) != 20:
            logger.error(f"Некорректная длина номера счета {len(digits_1)}")
            raise ValueError("Номер счёта должен содержать 20 цифр.")

        masked_account = "**" + digits_1[-4:]
        logger.info(f"Успешно замаскирован номер счета {masked_account}.")
        return masked_account

    except Exception as e:
        logger.exception(f"Ошибка при маскировке номера счета {e}.")
        raise
