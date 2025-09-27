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

