from decimal import Decimal, InvalidOperation


def format_decimal_number(number: Decimal) -> str:
    """
    Форматирует десятичное число для отображения.
    Убирает лишние нули и округляет до 2 знаков после запятой.
    """
    if number is None:
        return "0"

    number_str = format(number)
    # print(f"Format number: {number_str}")

    if '.' in number_str:
        integer_part, fractional_part = number_str.split('.')
        if not fractional_part or int(fractional_part) == 0:
            return integer_part or "0"

        # print(f"{integer_part=} // {fractional_part=}")

        first_non_zero_idx = len(fractional_part) - len(fractional_part.lstrip('0'))
        zero_count = first_non_zero_idx

        if zero_count > 3:
            significant_part = fractional_part[first_non_zero_idx: first_non_zero_idx + 2]
            return f"{integer_part}.|{zero_count}|{significant_part}"
        else:
            return str(round(float(number_str), 2))
    else:
        return number_str


def normalized_price_coin(coin):
    """Возвращает нормализованную цену."""
    if coin.price is not None:
        # print(coin.price)
        # print(coin.price.normalize())
        coin.format_price = format_decimal_number(coin.price.normalize())
    else:
        coin.format_price = None


# =============================================================================================================

def get_price_change(object_coin):
    # Если объект новый, изменение цены не вычисляем
    if object_coin.pk is None:
        object_coin.price_change_percentage = None
        return

    # Получаем старую цену из базы данных
    old = object_coin.__class__.objects.filter(pk=object_coin.pk).first()
    if old is None or old.price is None or object_coin.price is None:
        object_coin.price_change_percentage = None
        return

    try:
        # Приводим цены к Decimal
        old_price = Decimal(str(old.price))  # Используем str для безопасности
        new_price = Decimal(str(object_coin.price))  # Используем str для безопасности

        # Проверяем, что старая цена не равна нулю
        if old_price == 0:
            object_coin.price_change_percentage = None
            return

        # Вычисляем изменение цены в процентах
        change = (new_price - old_price) / old_price * 100
        direction = "asc" if change >= 0 else "desc"
        object_coin.price_change_percentage = f"{direction}, {abs(change):.2f}%"

    except (InvalidOperation, ZeroDivisionError, ValueError) as e:
        # Логируем ошибку, если необходимо
        print(f"Error calculating price change: {e}")
        object_coin.price_change_percentage = None

