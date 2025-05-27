import unittest
from io import StringIO
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.readers import read_financial_transactions


class TestReadFinancialTransactions(unittest.TestCase):

    @patch("pandas.read_csv")
    def test_read_csv_success(self, mock_read_csv: Any) -> None:
        mock_df = pd.DataFrame({"date": ["2024-01-01"], "amount": [100]})
        mock_read_csv.return_value = mock_df

        result = read_financial_transactions("dummy.csv")
        self.assertIsNotNone(result)

        assert result is not None
        self.assertTrue(result.equals(mock_df))
        mock_read_csv.assert_called_once_with("dummy.csv", sep=";", encoding="utf-8")

    @patch("pandas.read_csv", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_read_csv: Any) -> None:
        result = read_financial_transactions("missing.csv")
        self.assertIsNone(result)
        mock_read_csv.assert_called_once()

    @patch("pandas.read_csv", side_effect=ValueError("invalid CSV"))
    def test_generic_exception(self, mock_read_csv: Any) -> None:
        result = read_financial_transactions("bad.csv")
        self.assertIsNone(result)
        mock_read_csv.assert_called_once()

    def test_read_csv_with_stringio(self) -> None:
        csv_data = "date;amount\n2024-01-01;100"
        csv_file = StringIO(csv_data)

        with patch("pandas.read_csv", return_value=pd.read_csv(csv_file, sep=";", encoding="utf-8")) as mock_read:
            result = read_financial_transactions("dummy.csv")
            self.assertIsNotNone(result)  # Для unittest
            assert result is not None  # Для mypy

            self.assertEqual(result.iloc[0]["amount"], 100)
            mock_read.assert_called_once_with("dummy.csv", sep=";", encoding="utf-8")
