import json
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import mock_open as unittest_mock_open
from unittest.mock import patch

from src.utils import load_transactions


class TestUtils(unittest.TestCase):
    @patch("builtins.open", new_callable=unittest_mock_open)
    @patch.object(Path, "exists")  # Изменено на patch.object
    @patch("json.load")
    def test_load_transactions_success(
        self, mock_json_load: MagicMock, mock_exists: MagicMock, mock_file_open: MagicMock
    ) -> None:
        """Тест успешной загрузки транзакций из файла."""
        test_data = [{"id": 1}, {"id": 2}]
        mock_json_load.return_value = test_data

        expected_path = Path(__file__).parent.parent / "data" / "operations.json"
        mock_exists.return_value = True  # Файл существует

        result = load_transactions()

        self.assertEqual(result, test_data)

        mock_exists.assert_called_once_with()

        mock_file_open.assert_called_once_with(expected_path, "r", encoding="utf-8")

        mock_json_load.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch.object(Path, "exists")
    def test_load_transactions_file_not_found(self, mock_exists: MagicMock, mock_open: MagicMock) -> None:
        """Тест обработки случая отсутствия файла транзакций."""
        mock_exists.return_value = False

        result = load_transactions()

        self.assertEqual(result, [])

        mock_exists.assert_called_once_with()

        mock_open.assert_not_called()

    @patch("builtins.open", new_callable=unittest_mock_open, read_data="invalid json")
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_transactions_invalid_json(self, mock_exists: MagicMock, _: Any) -> None:
        """Тест обработки невалидного JSON."""
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            result = load_transactions()
            self.assertEqual(result, [])

    @patch("builtins.open", side_effect=PermissionError)
    @patch("pathlib.Path.exists", return_value=True)
    def test_load_transactions_permission_error(self, mock_open: MagicMock, _: Any) -> None:
        """Тест обработки ошибки доступа к файлу."""
        result = load_transactions()
        self.assertEqual(result, [])
