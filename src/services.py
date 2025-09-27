from pprint import pprint
import logging
from pathlib import Path
from src.utils import read_transactions_xlsx

MODULE_DIR = Path(__file__).resolve().parent
LOG_DIR = MODULE_DIR.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
log_file = LOG_DIR / "services.log"
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def simple_search(search_string: str, filepath: str) -> list[dict]:
    """Функция принимает строку для поиска и транзакции, возвращает json-ответ"""

    data = read_transactions_xlsx(filepath)

    new_data = []
    search_string_pattern = search_string.lower()
    for item in data:
        if search_string_pattern in str(item.get("Описание")).lower() or search_string_pattern in str(item.get("Категория")).lower():
            new_data.append(item)

    return new_data

pprint(simple_search("переводы", "../data/operations.xlsx"))

