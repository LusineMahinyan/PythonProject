from typing import Dict, List, Optional

import pandas as pd


def read_financial_transactions(csv_path: str) -> Optional[List[Dict]]:
    """Считывает финансовые операции из CSV-файла и возвращает список транзакций в виде словарей."""
    try:
        transactions_df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
        return transactions_df.to_dict("records")
    except FileNotFoundError:
        print(f"Ошибка: файл '{csv_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return None


df = pd.read_excel(r"C:\Users\PC\Downloads\transactions_excel.xlsx")
print(df.head())


def read_financial_transactions_excel(file_path: str) -> List[Dict]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей."""
    try:
        transactions_data = pd.read_excel(file_path)
        return transactions_data.to_dict(orient="records")
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
    return []
