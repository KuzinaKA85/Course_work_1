import json
import logging
import os
from pathlib import Path
import pandas as pd


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


def get_greeting(now_hour: int) -> str:
    """
    Функция возвращает приветствие в зависимости от текущего времени
    """
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
    """
    Функция для считывания финансовых операций из Excel
    """

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