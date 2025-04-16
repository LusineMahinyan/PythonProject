from typing import Any, Union

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("card_number, expected", [
    ("1596837868705199", "1596 83** **** 5199"),
    (7158300734726758, "7158 30** **** 6758"),
    ("7158-3007-3472-6758", "7158 30** **** 6758"),
    ("7158 3007 3472 6758", "7158 30** **** 6758"),
])
def test_get_mask_card_number(
        card_number: str,
        expected: str
) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("invalid_card_number", [
    "1234",
    "12345678901234567890",
    "1234-5678-9012-ABCD",
    " "
])
def test_invalid_card_number(invalid_card_number: Any) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_card_number)


@pytest.mark.parametrize("account_number, expected", [
    ("64686473678894779589", "**9589"),
    (64686473678894779589, "**9589"),
    ("6468 6473 6788 9477 9589", "**9589"),
    ("6468-6473-6788-9477-9589", "**9589"),
])
def test_valid_account_numbers(
        account_number: str,
        expected: str
) -> None:
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("invalid_account_number", [
    "123",
    "ABC123",
    "",
    "12 34 56 78 9",
])
def test_invalid_account_number(
        invalid_account_number: Union
) -> None:
    with pytest.raises(ValueError):
        get_mask_account(invalid_account_number)
