import pytest

from src.filters import filter_by_description, filter_by_status


@pytest.fixture
def mock_data():
    return [
        {"description": "Оплата интернета", "status": "EXECUTED", "amount": "1200 руб.", "date": "2020-01-01"},
        {"description": "Перевод", "status": "PENDING", "amount": "900 USD", "date": "2020-01-02"},
    ]


def test_filter_by_description(mock_data):
    result = filter_by_description(mock_data, "интернет")
    assert len(result) == 1


def test_filter_by_status(mock_data):
    result = filter_by_status(mock_data, "executed")
    assert len(result) == 1
