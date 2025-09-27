from unittest.mock import patch

from src.services import simple_search


@patch("src.services.read_transactions_xlsx")
def test_search_by_description(mock_read_xlsx):
    """Тест поиска по описанию"""
    mock_data = [
        {"Описание": "Покупка в магазине", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Оплата такси", "Категория": "Транспорт", "Сумма": -50},
        {"Описание": "Кинотеатр", "Категория": "Развлечения", "Сумма": -30},
    ]
    mock_read_xlsx.return_value = mock_data

    result = simple_search("магазин", "test.xlsx")

    expected = [{"Описание": "Покупка в магазине", "Категория": "Еда", "Сумма": -100}]
    assert result == expected


@patch("src.services.read_transactions_xlsx")
def test_search_by_category(mock_read_xlsx):
    """Тест поиска по категории"""
    mock_data = [
        {"Описание": "Покупка в магазине", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Оплата такси", "Категория": "Транспорт", "Сумма": -50},
        {"Описание": "Кинотеатр", "Категория": "Развлечения", "Сумма": -30},
    ]
    mock_read_xlsx.return_value = mock_data

    result = simple_search("транспорт", "test.xlsx")

    expected = [{"Описание": "Оплата такси", "Категория": "Транспорт", "Сумма": -50}]
    assert result == expected


@patch("src.services.read_transactions_xlsx")
def test_case_insensitive_search(mock_read_xlsx):
    """Тест поиска без учета регистра"""
    mock_data = [
        {"Описание": "Покупка в Магазине", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Оплата Такси", "Категория": "Транспорт", "Сумма": -50},
    ]
    mock_read_xlsx.return_value = mock_data

    # Поиск в нижнем регистре
    result1 = simple_search("магазин", "test.xlsx")
    # Поиск в верхнем регистре
    result2 = simple_search("МАГАЗИН", "test.xlsx")
    # Поиск в смешанном регистре
    result3 = simple_search("МаГаЗиН", "test.xlsx")

    expected = [{"Описание": "Покупка в Магазине", "Категория": "Еда", "Сумма": -100}]
    assert result1 == expected
    assert result2 == expected
    assert result3 == expected


@patch("src.services.read_transactions_xlsx")
def test_multiple_matches(mock_read_xlsx):
    """Тест когда несколько результатов соответствуют поиску"""
    mock_data = [
        {"Описание": "Магазин продуктов", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Онлайн магазин", "Категория": "Покупки", "Сумма": -200},
        {"Описание": "Такси", "Категория": "Транспорт", "Сумма": -50},
    ]
    mock_read_xlsx.return_value = mock_data

    result = simple_search("магазин", "test.xlsx")

    expected = [
        {"Описание": "Магазин продуктов", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Онлайн магазин", "Категория": "Покупки", "Сумма": -200},
    ]
    assert result == expected


@patch("src.services.read_transactions_xlsx")
def test_no_matches(mock_read_xlsx):
    """Тест когда нет совпадений"""
    mock_data = [
        {"Описание": "Покупка в магазине", "Категория": "Еда", "Сумма": -100},
        {"Описание": "Оплата такси", "Категория": "Транспорт", "Сумма": -50},
    ]
    mock_read_xlsx.return_value = mock_data

    result = simple_search("ресторан", "test.xlsx")
    assert result == []
