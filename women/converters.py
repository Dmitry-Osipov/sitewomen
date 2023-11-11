class FourDigitYearConverter:
    """
    Класс служит для отлавливания года, который передаётся в функцию представления archive.
    """
    regex = '[0-9]{4}'  # Регулярное выражение.

    def to_python(self, value: str) -> int:
        """
        Метод служит для преобразования строки значения года в число.

        :param value: год, введённый пользователем в формате строки.
        :return: год, введённый пользователем в формате числа
        """
        return int(value)

    def to_url(self, value: int) -> str:
        """
        Метод служит для преобразования целого значения в строку для URL.

        :param value: год, введённый пользователем в формате числа.
        :return: год, введённый пользователем в формате строки.
        """
        return '$04d' % value