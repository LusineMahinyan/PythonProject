import json
import logging
from pathlib import Path

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions():
    """Загружает список транзакций из файла data/operations.json."""
    logging.debug("Начало загрузки транзакции.")

    file_path = Path(__file__).parent.parent / "data" / "operations.json"
    logging.debug(f"Попытка загрузить файл: {file_path}")

    if not file_path.exists():
        logging.debug(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                logging.error("Загруженные данные не являются списком")
                return []

            if not all(isinstance(item, dict) for item in data):
                logging.error("Не все элементы в списке являются словарями")
                return []

            logging.info(f"Успешно загружено {len(data)} транзакций.")
            return data

    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON: {e}")
        return []
    except PermissionError as e:
        logging.error(f"Ошибка доступа к файлу: {e}")
        return []
    except Exception as e:
        logging.exception(f"Неожиданная ошибка при загрузке транзакций: {e}")
        return []
    finally:
        logging.debug("Завершение загрузки транзакций.")
