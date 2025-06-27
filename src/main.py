import csv
import json
from typing import Any, Dict, List, cast

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from src.filters import filter_by_currency, filter_by_description, filter_by_status, sort_by_date
from src.formatter import print_transactions


def load_from_json(path: str) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Ожидался список транзакций")
    return data


def load_from_csv(path: str) -> List[Dict[str, str]]:
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_from_xlsx(path: str) -> List[Dict[str, Any]]:
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active

    if sheet is None or not isinstance(sheet, Worksheet):
        raise ValueError("Не удалось загрузить активный лист")

    keys = [str(cell.value) if cell.value is not None else "" for cell in sheet[1]]

    rows = [dict(zip(keys, [cell.value for cell in row])) for row in sheet.iter_rows(min_row=2)]

    return cast(List[Dict[str, Any]], rows)


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")
    if choice == "1":
        transactions = load_from_json("transactions.json")
        print("Программа: Для обработки выбран JSON-файл.")
    elif choice == "2":
        transactions = load_from_csv("transactions.csv")
        print("Программа: Для обработки выбран CSV-файл.")
    elif choice == "3":
        transactions = load_from_xlsx("transactions.xlsx")
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Программа: Неверный выбор.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию. "
            "\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
        )
        if status.upper() not in valid_statuses:
            print(f'Программа: Статус операции "{status}" недоступен.')
            continue
        break

    transactions = filter_by_status(transactions, status)
    print(f'Программа: Операции отфильтрованы по статусу "{status.upper()}"')

    sort_input = input("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
    if sort_input == "да":
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        ascending = order == "по возрастанию"
        transactions = sort_by_date(transactions, ascending)

    currency_filter = input("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
    if currency_filter == "да":
        transactions = filter_by_currency(transactions)

    desc_filter = (
        input("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ")
        .strip()
        .lower()
    )
    if desc_filter == "да":
        keyword = input("Введите слово для поиска: ").strip()
        transactions = filter_by_description(transactions, keyword)

    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    if transactions:
        print_transactions(transactions)
    else:
        print("\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


if __name__ == "__main__":
    main()
