import json
import logging
import os
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv


MODULE_DIR = Path(__file__).resolve().parent
LOG_DIR = MODULE_DIR.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_file = LOG_DIR / "utils.log"
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

load_dotenv("../.env")

API_KEY_FOR_CURRENT_EXCHANGE_RATE = os.getenv("API_KEY_FOR_CURRENT_EXCHANGE_RATE")
API_KEY_ALPHA_VANTAGE = os.getenv("API_KEY_ALPHA_VANTAGE")


def get_greeting(now_hour: int) -> str:
    """ Функция возвращает приветствие в зависимости от текущего времени """
    message = ""

    if 6 <= now_hour < 12:
        message = "Доброе утро!"
    elif 12 <= now_hour < 18:
        message = "Добрый день!"
    elif 18 <= now_hour < 24:
        message = "Добрый вечер!"
    else:
        message = "Доброй ночи!"

    return message


def read_transactions_xlsx(file_path: str) -> list[dict]:
    """ Функция для считывания финансовых операций из Excel """

    if not os.path.exists(file_path):
        logger.warning("Файл не найден")
        return []

    if os.path.getsize(file_path) == 0:
        logger.warning("Файл пуст")
        return []

    logger.info(f"Чтение файла из: {file_path}")
    xlsx_data = pd.read_excel(file_path)
    xlsx_data_dict = xlsx_data.to_dict(orient="records")

    if isinstance(xlsx_data_dict, list):
        return xlsx_data_dict
    else:
        logger.warning("Файл содержит не список")
        return []

# file_path_1 = Path("..", "data", "operations.xlsx")
# print(read_transactions_xlsx(file_path_1))

def load_json_data(file_path: str) -> dict:
    """ Функция возвращает данные о финансовых транзакциях из JSON """

    try:
        if not os.path.exists(file_path):
            logger.warning("Файл не найден")
            return {}

        if os.path.getsize(file_path) == 0:
            logger.warning("Файл пуст")
            return {}

        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f"Чтение файла из: {file_path}")
            data = json.load(file)

        if isinstance(data, dict):
            return data
        else:
            logger.warning("Файл содержит данные не в json-формате")
            return {}

    except (json.JSONDecodeError, FileNotFoundError, PermissionError, OSError):
        logger.error("Некорректные данные")
        return {}

# file_path_2 = Path("..", "user_settings.json")
# print(load_json_data(file_path_2))


def get_last_four(input_string: str) -> str:
    """ Функция для возвращения последний четырёх символов """

    if input_string:
        return input_string[-4:]
    return "None"


def get_cashback(total_spent: float) -> float:
    """ Функция для расчёта кешбека """

    return round((total_spent / 100), 2)


def filter_by_state(data: list[dict], state: str = "OK") -> list[dict]:
    """ Фильтрует список словарей по значению ключа 'state' """

    if not data:
        raise ValueError("Пустой список")

    new_data = list()

    for item in data:
        if item.get("Статус") == state:
            new_data.append(item)

    return new_data


def get_card_infos(transactions: list[dict]) -> list[dict]:
    """ Возвращает инфомацию о картах """

    if not transactions:
        return []

    df = pd.DataFrame(transactions)

    cards = []

    negative_df = df[df["Сумма платежа"] < 0]
    data = negative_df.groupby("Номер карты")["Сумма платежа"].sum()

    for card_number, total_amount in data.items():

        card_number = get_last_four(str(card_number))
        total_spent = abs(round(total_amount, 2))
        cashback = get_cashback(total_spent)
        card_info = dict(last_digits=card_number, total_spent=total_spent, cashback=cashback)
        cards.append(card_info)

    return cards


def get_top_transactions(transactions: list[dict]) -> list[dict]:
    """ Выводит топ топ-5 транзакций по сумме платежа """

    data = sorted(transactions, key=lambda x: abs(x["Сумма платежа"]), reverse=True)[:5]
    result = []
    for i, transaction in enumerate(data, 1):
        transaction_info = dict(
            date=transaction["Дата платежа"],
            amount=transaction["Сумма платежа"],
            category=transaction["Категория"],
            description=transaction["Описание"],
        )
        result.append(transaction_info)
    return result


def get_current_exchange_rate(currency_codes: list) -> list:
    """ Функция возврата текущего курса """

    url = "https://api.apilayer.com/exchangerates_data/latest"

    headers = {"apikey": API_KEY_FOR_CURRENT_EXCHANGE_RATE}
    result = []
    for code in currency_codes:
        params = {"symbols": "RUB", "base": code}
        response = requests.get(url, headers=headers, params=params)
        response_to_float = float(response.json()["rates"]["RUB"])

        currency_code_info = dict(currency=code, rate=round(response_to_float, 2))
        result.append(currency_code_info)

    return result


def get_stock(stocks: list) -> list:
    """ Функция возврата текущего курса """

    url = "https://www.alphavantage.co/query"

    result = []
    for stock in stocks:
        params = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": API_KEY_ALPHA_VANTAGE}
        response = requests.get(url, params=params)

        global_quote = response.json().get("Global Quote")
        if global_quote is not None:
            response_to_float = float(response.json()["Global Quote"]["05. price"])
            stocks_info = dict(stock=stock, price=round(response_to_float, 2))
            result.append(stocks_info)
        else:
            logger.warning(f"The request ended with an error {response.json()}")
            result.append(response.json())

    return result
