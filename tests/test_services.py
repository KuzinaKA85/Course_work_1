import json
from unittest.mock import patch

from src.services import simple_search


@patch("src.services.read_transactions_xlsx")
def test_search_returns_valid_json_string(mock_read_xlsx):
    """Тест что функция возвращает валидную JSON строку"""
    # Мокаем данные
    mock_data = [
        {"Описание": "Покупка в магазине", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Оплата такси", "Категория": "Транспорт", "Сумма": -50},
    ]
    mock_read_xlsx.return_value = mock_data

    result = simple_search("магазин", "test.xlsx")

    # Проверяем что это строка
    assert isinstance(result, str)

    # Проверяем что это валидный JSON
    parsed_result = json.loads(result)
    assert len(parsed_result) == 1
    assert parsed_result[0]["Описание"] == "Покупка в магазине"


@patch("src.services.read_transactions_xlsx")
def test_search_by_description(mock_read_xlsx):
    """Тест поиска по описанию"""
    mock_data = [
        {"Описание": "Покупка в магазине", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Кинотеатр", "Категория": "Развлечения", "Сумма": -50},
    ]
    mock_read_xlsx.return_value = mock_data

    result = simple_search("кино", "test.xlsx")
    parsed_result = json.loads(result)

    assert len(parsed_result) == 1
    assert parsed_result[0]["Описание"] == "Кинотеатр"
    assert parsed_result[0]["Категория"] == "Развлечения"


@patch("src.services.read_transactions_xlsx")
def test_search_by_category(mock_read_xlsx):
    """Тест поиска по категории"""
    mock_data = [
        {"Описание": "Покупка в магазине", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Оплата такси", "Категория": "Транспорт", "Сумма": -50},
    ]
    mock_read_xlsx.return_value = mock_data

    result = simple_search("транспорт", "test.xlsx")
    parsed_result = json.loads(result)

    assert len(parsed_result) == 1
    assert parsed_result[0]["Категория"] == "Транспорт"
