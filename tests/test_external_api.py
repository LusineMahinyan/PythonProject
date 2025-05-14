import unittest
from unittest.mock import MagicMock, patch

import requests

from src.external_api import convert_to_rub


class TestExternalAPI(unittest.TestCase):
    @patch("src.external_api.requests.get")
    @patch("src.external_api.API_KEY", "test_api_key")
    def test_convert_to_rub_success(self, mock_get: MagicMock) -> None:
        """Тест успешной конвертации валюты в рубли."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"RUB": 75.5}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = convert_to_rub(100, "USD")

        self.assertEqual(result, 7550.0)
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest",
            params={"base": "USD", "symbols": "RUB"},
            headers={"apikey": "test_api_key"},
            timeout=5,
        )

    @patch("src.external_api.requests.get")
    @patch("src.external_api.API_KEY", None)
    def test_convert_to_rub_no_api_key(self, mock_get: MagicMock) -> None:
        """Тест проверяет вызов ValueError при отсутствии API-ключа."""
        with self.assertRaises(ValueError) as context:
            convert_to_rub(100, "USD")

        self.assertEqual(str(context.exception), "API key not configured. Check .env file")

        mock_get.assert_not_called()

    @patch("os.getenv")
    def test_convert_to_rub_rub(self, mock_getenv: MagicMock) -> None:
        """Тест обработки транзакций в рублях (без конвертации)."""
        mock_getenv.return_value = "test_api_key"
        result = convert_to_rub(100, "RUB")
        self.assertEqual(result, 100)

    @patch("os.getenv")
    @patch("requests.get")
    def test_convert_to_rub_api_error(
            self,
            mock_get: MagicMock,
            mock_getenv: MagicMock
    ) -> None:
        """Тест обработки ошибки при запросе к API конвертации валют."""
        mock_getenv.return_value = "test_api_key"
        mock_get.side_effect = requests.RequestException("API error")
        result = convert_to_rub(100, "USD")
        self.assertIsNone(result)
