import json
from pathlib import Path
from typing import List, Dict


def load_transactions() -> List[Dict]:
    """Загружает список транзакций из файла data/operations.json."""
    file_path = Path(__file__).parent.parent / "data" / "operations.json"

    # Явно создаем Path объект и вызываем exists()
    if not file_path.exists():
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, PermissionError) as e:
        print(f"Error loading transactions: {e}")
        return []