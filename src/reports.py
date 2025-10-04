import json
import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional, Union

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import filter_by_date, get_date


def name_default(func: Callable) -> str:
    """Функция генерирует имя файла для отчета"""

    return f"../reports/report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"


def report_writer(arg: Optional[Union[str, Callable]] = None) -> Callable:
    """Декоратор для логирования результата функции"""

    if callable(arg):
        func = arg

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка для функции при использовании @report_writer без аргументов."""

            result = func(*args, **kwargs)
            json_write(name_default(func), result)
            return result

        return wrapper

    filename = None if arg is None else str(arg)

    def decorator(func: Callable) -> Callable:
        """Декоратор для функции при использовании @report_writer с аргументами."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обертка для функции при использовании @report_writer с аргументами."""
            result = func(*args, **kwargs)
            json_write(filename or name_default(func), result)
            return result

        return wrapper

    return decorator


def json_write(filename: str, result: Any) -> None:
    """Функция сохраняет данные в JSON файл с автоматическим созданием папок"""
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    if pd is not None and isinstance(result, pd.DataFrame):
        result.to_json(filename, orient="records", force_ascii=False, indent=2)
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


@report_writer()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция формирует результат - отчет в виде DataFrame"""

    end_date = datetime.now()
    if date is not None:
        end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()

    start_date = end_date - relativedelta(months=3)

    start_date_formated = datetime.strftime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date_formated = datetime.strftime(end_date, "%Y-%m-%d %H:%M:%S")

    start_date_str = get_date(start_date_formated)
    end_date_str = get_date(end_date_formated)

    transactions_list = transactions.to_dict(orient="records")
    data_filtered = filter_by_date(transactions_list, start_date_str, end_date_str)

    data = pd.DataFrame(data_filtered)

    category_data = data[data["Категория"] == category]
    result = pd.DataFrame(category_data)
    return result
