import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from src.readers import read_financial_transactions, read_financial_transactions_excel


class TestReadFinancialTransactions(unittest.TestCase):
    """Тесты для функции read_financial_transactions с использованием Mock и patch."""

    @patch("pandas.read_csv")
    def test_read_csv_success(self, mock_read_csv: MagicMock) -> None:
        """Успешное чтение CSV: возвращается список словарей."""
        mock_df = MagicMock(spec=pd.DataFrame)
        mock_df.to_dict.return_value = [{"date": "2024-01-01", "amount": 100}]
        mock_read_csv.return_value = mock_df
        result = read_financial_transactions("dummy.csv")
        mock_read_csv.assert_called_once_with("dummy.csv", sep=";", encoding="utf-8")
        mock_df.to_dict.assert_called_once_with("records")
        self.assertEqual(result, [{"date": "2024-01-01", "amount": 100}])

    @patch("pandas.read_csv", side_effect=FileNotFoundError)
    def test_file_not_found_error(self, mock_read_csv: MagicMock) -> None:
        """Обработка ошибки FileNotFoundError."""
        result = read_financial_transactions("missing.csv")
        self.assertIsNone(result)
        mock_read_csv.assert_called_once_with("missing.csv", sep=";", encoding="utf-8")

    @patch("pandas.read_csv", side_effect=Exception("Invalid CSV"))
    def test_generic_error_handling(self, mock_read_csv: MagicMock) -> None:
        """Обработка прочих ошибок."""
        result = read_financial_transactions("corrupted.csv")
        self.assertIsNone(result)
        mock_read_csv.assert_called_once_with("corrupted.csv", sep=";", encoding="utf-8")

    @patch("pandas.read_csv")
    def test_empty_csv_returns_empty_list(self, mock_read_csv: MagicMock) -> None:
        """Пустой CSV должен возвращать пустой список."""
        mock_df = MagicMock(spec=pd.DataFrame)
        mock_df.to_dict.return_value = []
        mock_read_csv.return_value = mock_df

        result = read_financial_transactions("empty.csv")
        self.assertEqual(result, [])


class TestReadFinancialTransactionsExcel(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_read_excel_success(self, mock_read_excel: MagicMock) -> None:
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [{"date": "2024-01-01", "amount": 100}]
        mock_read_excel.return_value = mock_df

        result = read_financial_transactions_excel("dummy.xlsx")

        self.assertEqual(result, [{"date": "2024-01-01", "amount": 100}])
        mock_read_excel.assert_called_once_with("dummy.xlsx")

    @patch("pandas.read_excel", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_read_excel: MagicMock) -> None:
        result = read_financial_transactions_excel("missing.xlsx")
        self.assertEqual(result, [])
        mock_read_excel.assert_called_once_with("missing.xlsx")

    @patch("pandas.read_excel", side_effect=ValueError("Invalid format"))
    def test_read_excel_generic_error(self, mock_read_excel: MagicMock) -> None:
        result = read_financial_transactions_excel("broken.xlsx")
        self.assertEqual(result, [])
        mock_read_excel.assert_called_once_with("broken.xlsx")
