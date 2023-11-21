from typing import Any

# Опишем главное меню сайта с помощью списка из словарей с маршрутом к соответствующей странице:
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
]


class DataMixin:
    """
    Базовый класс предназначен для ликвидации дублирования кода в дочерних классах представления.

    Атрибуты:\n
    title_page - str - заголовок страницы;\n
    cat_selected - int - рубрика поста;\n
    extra_context - dict - контекст для отображения на странице (например, меню, заголовок и т.п.);\n
    paginate_by - int - количество записей, отображаемых на одной странице.
    """
    title_page = None
    cat_selected = None
    extra_context = {}
    paginate_by = 5

    def __init__(self):
        """
        Инициализатор класса отвечает за заполнение словаря extra_context.
        """
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        """
        Метод определяет словарь с заранее заданными ключами для метода get_context_data дочерних классов.

        :param context: Словарь для шаблона.
        :param kwargs: Дополнительные параметры в формате ключ-значение.
        :return: Словарь шаблона.
        """
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
