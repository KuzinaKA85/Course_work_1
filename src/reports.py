# import functools
# import json
# from datetime import datetime
#
# import pandas as pd
# from typing import Optional, Callable
#
# from dateutil.relativedelta import relativedelta
#
# from src.utils import get_date, filter_by_date
#
# def log(filename: Optional[str] = None) -> Callable:
#
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             """
#             Обертка, которая собственно выполняет функцию
#             и логирует результат или ошибку
#             """
#             try:
#                 result = func(*args, **kwargs)
#                 message = f"{func.__name__} ok"
#                 if filename:
#                     with open(filename, "w", encoding="utf-8") as f:
#                         json.dump(result, f, ensure_ascii=False, indent=2)
#                 else:
#                     print(message)
#                 return result
#             except Exception as e:
#                 error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
#                 if filename:
#                     with open(filename, "w", encoding="utf-8") as f:
#                         f.write(error_message + "\n")
#                 else:
#                     print(error_message)
#                     raise
#         return wrapper
#     return decorator
#
# @log(filename="log.json")
# def spending_by_category(transactions: pd.DataFrame,
#                          category: str,
#                          date: Optional[str] = None) -> pd.DataFrame:
#     end_date = datetime.now()
#     if date is not None:
#         end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
#
#     start_date = end_date - relativedelta(months=3)
#
#     start_date_formated = datetime.strftime(start_date, "%Y-%m-%d %H:%M:%S")
#     end_date_formated = datetime.strftime(end_date, "%Y-%m-%d %H:%M:%S")
#
#     start_date_str = get_date(start_date_formated)
#     end_date_str = get_date(end_date_formated)
#
#     transactions_list = transactions.to_dict(orient="records")
#     data_filtered = filter_by_date(transactions_list, start_date_str, end_date_str)
#
#     data = pd.DataFrame(data_filtered)
#
#     category_data = data[data["Категория"] == category]
#     result = pd.DataFrame(category_data)
#     return result
#



import json
import os

from src.utils import get_date, filter_by_date

import pandas as pd
from dateutil.relativedelta import relativedelta

# import datetime

from functools import wraps
from datetime import datetime
from typing import Optional

def name_default(func):
    return f"../reports/report_{func.__name__}.json"

def report_writer(arg=None):
    if callable(arg):  # @report_writer
        func = arg
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            json_write(name_default(func), result)
            return result
        return wrapper

    filename = None if arg is None else str(arg)

    def decorator(func):  # @report_writer("file.json") или @report_writer()
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            json_write(filename or name_default(func), result)
            return result
        return wrapper
    return decorator

def json_write(filename, result):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    if pd is not None and isinstance(result, pd.DataFrame):
        result.to_json(filename, orient="records", force_ascii=False, indent=2)  # [web:46]
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)  # [web:3]


@report_writer()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
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


