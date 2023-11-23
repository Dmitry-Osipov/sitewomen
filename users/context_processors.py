from django.http import HttpRequest

from women.utils import menu


def get_women_context(request: HttpRequest) -> dict[str, list[dict[str, str]]]:
    """
    Контекстный процессор служит для передачи главного меню в шаблоны. Контекстный процессор имеет смысл использовать,
    только если мы передаём данные во все, или почти все, шаблоны. В противном случае требуется использовать функцию
    render.

    :param request: Запрос.
    :return: Словарь с меню сайта.
    """
    return {'mainmenu': menu}
