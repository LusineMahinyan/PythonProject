import pandas as pd
from pandas import DataFrame
from typing import Optional

def read_financial_transactions(csv_path: str) -> Optional[DataFrame]:
    """Считывает финансовые операции из CSV-файла и возвращает DataFrame."""
    try:
        df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
        return df
    except FileNotFoundError:
        print(f"Ошибка: файл '{csv_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return None
