import json
from pathlib import Path
from typing import List, Dict

def load_transactions() -> List[Dict]:
    """Загружает список транзакций из файла data/operations.json."""
    file_path = Path(__file__).parent.parent / 'data' / 'operations.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception as e:
        print(f"Произошла ошибка при загрузке файла: {e}")
        return []


if __name__ == "__main__":
    transactions = load_transactions()
    print(f"Загружено {len(transactions)} транзакций")
    print("Первые 3 транзакции:", transactions[:3])