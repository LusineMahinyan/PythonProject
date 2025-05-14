import unittest
from unittest.mock import MagicMock, patch

from src.transactions import convert_to_rub


class TestTransactions(unittest.TestCase):
    @patch("src.transactions.convert_to_rub")
    def test_convert_to_rub_foreign(self, mock_convert: MagicMock) -> None:
        mock_convert.return_value = 7500.0

        transaction = {"amount": "100", "currency": "USD"}

        from src.transactions import convert_to_rub
        result = convert_to_rub(transaction)

        self.assertEqual(result, 7500.0)

    def test_convert_to_rub_rub(self) -> None:
        transaction = {"amount": "100", "currency": "RUB"}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 100.0)

    def test_convert_to_rub_no_currency(self) -> None:
        transaction = {"amount": "100"}
        result = convert_to_rub(transaction)
        self.assertEqual(result, 100.0)

    def test_convert_to_rub_invalid_amount(self) -> None:
        transaction = {"amount": "invalid", "currency": "USD"}
        result = convert_to_rub(transaction)
        self.assertIsNone(result)

    def test_convert_to_rub_missing_amount(self) -> None:
        transaction = {"currency": "USD"}
        result = convert_to_rub(transaction)
        self.assertIsNone(result)
