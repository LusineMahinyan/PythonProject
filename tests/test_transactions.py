import unittest
from unittest.mock import MagicMock, patch

from src.transactions import get_transaction_amount_rub


class TestTransactions(unittest.TestCase):
    @patch("src.transactions.convert_to_rub")
    def test_get_transaction_amount_rub_foreign(self, mock_convert: MagicMock) -> None:
        mock_convert.return_value = 7500.0
        transaction = {"amount": "100", "currency": "USD"}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 7500.0)

    def test_get_transaction_amount_rub_rub(self) -> None:
        transaction = {"amount": "100", "currency": "RUB"}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 100.0)

    def test_get_transaction_amount_rub_no_currency(self) -> None:
        transaction = {"amount": "100"}
        result = get_transaction_amount_rub(transaction)
        self.assertEqual(result, 100.0)

    def test_get_transaction_amount_rub_invalid_amount(self) -> None:
        transaction = {"amount": "invalid", "currency": "USD"}
        result = get_transaction_amount_rub(transaction)
        self.assertIsNone(result)

    def test_get_transaction_amount_rub_missing_amount(self) -> None:
        transaction = {"currency": "USD"}
        result = get_transaction_amount_rub(transaction)
        self.assertIsNone(result)
