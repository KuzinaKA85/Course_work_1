from pprint import pprint

import pandas as pd

from src.services import simple_search
from src.utils import read_transactions_xlsx
from src.reports import spending_by_category
from src.views import main_page


# Проверяем работу модуля views
print("Проверка работы модуля views")
print(main_page("2021-12-31 16:44:00"))

# Проверяем работу модуля services
print("Проверка работу модуля services")
pprint(simple_search("переводы", "../data/operations.xlsx"))

# Проверяем работу модуля reports
print("Проверка работу модуля reports")
data = read_transactions_xlsx("../data/operations.xlsx")
df = pd.DataFrame(data)
print(spending_by_category(df, "Супермаркеты", "2021-09-12 16:15:15"))
