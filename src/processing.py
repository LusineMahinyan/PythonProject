from typing import Dict, Any


operations = [
    {
        'id': 41428829,
        'state': 'EXECUTED',
        'date': '2019-07-03T18:35:29.512364'
    },
    {
        'id': 939719570,
        'state': 'EXECUTED',
        'date': '2018-06-30T02:08:58.425572'
    },
    {
        'id': 594226727,
        'state': 'CANCELED',
        'date': '2018-09-12T21:27:25.241689'
    },
    {
        'id': 615064591,
        'state': 'CANCELED',
        'date': '2018-10-14T08:21:33.419441'
    }
]


def filter_by_state(
        operations: list[dict[str, any]],
        state: str = "EXECUTED"
) -> list[dict[str, any]]:
    """Фильтрует список словарей по значениб state"""
    result = []
    for operation in operations:
        if operation.get("state") == state:
            result.append(operation)
    return result


# print(filter_by_state(operations, state="EXECUTED"))
# print(filter_by_state(operations, state="CANCELED"))


def sort_by_date(
    data: list[Dict[str, Any]],
    reverse: bool = True
) -> list[Dict[str, Any]]:
    """Сортирует список словарей по дате"""
    return sorted(data, key=lambda x: x['date'], reverse=reverse)

# print(sort_by_date(operations))
