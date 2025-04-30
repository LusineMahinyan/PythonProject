# Проект "PythonProject"

## Описание:

Проект предоставляет функции для обработки операций:
1. В файле "masks":\
-Функция маскировки номера банковской карты;\
-Функция, которая принимает на вход номер счета и возвращает его маску,
2. В файле "processing":\
-Функция, которая фильтрует список словарей по значению state;\
-Функция сортирует список словарей по дате,
3. В файле "widget":\
-Функция кодировки счета/карты;\
-Функция для преобразования даты и времени в формат ДД.ММ.ГГГГ.
4. В файле "generators":\
-Генератор фильтрует транзакции по коду валюты;\
-Генератор, который возвращает описания транзакций по очереди;\
-Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.


## Установка и использование:
1. Клонируйте репозиторий:\
```git clone git@github.com:ваш-username/PythonProject.git```
2. Импортируйте нужные функции в свой проект:\
```from masks import get_mask_card_number, get_mask_account```\
```from processing import filter_by_state, sort_by_date```\
```from widget import mask_account_card, get_date```
```from generators import card_number_generator, filter_by_currency, transaction_descriptions```


## Функционал

1. Модуль masks.py \
-get_mask_card_number(card_number: int) -> str \
Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.\
Пример: \
```get_mask_card_number(7000792289606361) #Возвращает "7000 79** **** 6361"```\
-get_mask_account(account_number: int) -> str \
Маскирует номер счета, оставляя видимыми только последние 4 цифры.\
Пример: \
```get_mask_account(73654108430135874305) #Возвращает "**4305"```
2. Модуль processing.py\
-filter_by_state(
        operations: list[dict[str, any]],
        state: str = "EXECUTED"
) -> list[dict[str, any]]: \
Фильтрует список операций по статусу выполнения. \
Пример: \ 
```filter_by_state([{"state": "EXECUTED"}, {"state": "PENDING"}], "EXECUTED")```
```#Возвращает "[{"state": "EXECUTED"}]"```\
-sort_by_date(
    data: list[Dict[str, Any]],
    reverse: bool = True
) -> list[Dict[str, Any]] \
Сортирует транзакции по дате (по умолчанию - от новых к старым). \
Пример: \
```sort_by_date([{"date": "2023-01-01"}, {"date": "2023-01-02"}])```
```#Возвращает "[{"date": "2023-01-02"}, {"date": "2023-01-01"}]"```
3. Модуль widget.py \
-mask_account_card(string: str) -> str \
Определяет тип финансового инструмента (карта/счет) и применяет соответствующую маскировку. \
Пример: \
```mask_account_card("Maestro 1596837868705199") #Возвращает "Maestro 1596 83** **** 5199" ``` \
```mask_account_card("Счет 64686473678894779589") #Возвращает "Счет **9589"``` \
-get_date(date_time: str) -> str \
Преобразует дату из формата ISO в русский формат (ДД.ММ.ГГГГ). \
Пример: \
```get_date("2024-03-11T02:26:18.671407") #Возвращает "11.03.2024"```
4. Модуль generators.py \
Модуль generators.py содержит набор генераторов для работы с банковскими транзакциями и генерации номеров карт.
-filter_by_currency(transactions, currency_code) -> Iterator[Dict] \
Фильтрует транзакции по коду валюты. \
Пример: 
```bash
usd_transactions = filter_by_currency(transactions, "USD") 
for tx in usd_transactions:
print(tx["description"]) 
```
-transaction_descriptions(transactions) -> Iterator[str] \
Генератор описаний транзакций.
Пример: 
```bash
for desc in transaction_descriptions(transactions):
    print(desc)
```
-card_number_generator(start, end) -> Generator[str, None, None] \
Генератор номеров банковских карт. \
Пример: 
```bash
for card_num in card_number_generator(1, 5):
    print(card_num)
```

## Требования
-Python 3.8+ \
-Зависимости отсутствуют (чистый Python)

## Лицензия
Проект распространяется под лицензией MIT.

##  Тестирование

Проект включает комплексные тесты для всех ключевых функций. 

### Структура тестов
tests/ \
├── test_masks.py # Тесты маскировок \
├── test_widgets.py # Тесты виджетов \
├── test_processing.py # Тесты обработки данных \
└── test_generators.py # Генераторы 

### Запуск тестов

```bash
pytest tests/ -v          # Все тесты с подробным выводом
pytest --cov=src          # С проверкой покрытия кода
```

