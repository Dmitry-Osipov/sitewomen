from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/women/.

    :param request: Ссылка на специальный класс, который называется HttpRequest и содержит информацию о запросе. Через
    эту переменную нам доступна вся информация о запросе.
    :return: Экземпляр класса HttpResponse, который автоматически формирует нужный заголовок ответа (содержимое ответа
    передаётся строкой аргументом).
    """
    return HttpResponse('Страница приложения women.')


def categories(request, cat_id):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/cat/<число>/.

    :param request: HttpRequest - запрос пользователя.
    :param cat_id: int - Уникальный идентификатор записи.
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Пользователь получает число, которое вводит в
    запросе. Прим.: HTML-теги не экранируются.
    """
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/cat/<слаг>/.

    :param request: HttpRequest - запрос пользователя.
    :param cat_slug: str - Уникальный идентификатор записи.
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Пользователь получает слаг, который вводит в
    запросе.
    """
    if request.GET:  # Словарь GET содержит параметры запроса в формате ключ=значение.
        print(request.GET)  # <QueryDict: {'name': ['gagrina'], 'type': ['pop']}>
        # <QueryDict: {'name': ['gagrina'], 'type': ['pop']}>
    if request.POST:  # Словарь POST содержит параметры передачи в том же самом классе.
        print(request.POST)
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')


def archive(request, year):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/cat/<слаг>/.

    :param request: HttpRequest - запрос пользователя.
    :param year: int - год, принадлежащий промежутку [1000;9999].
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Пользователь получает год, который вводит в
    запросе.
    """
    if year > 2023:
        raise Http404()  # Когда активизируется механизм обработки 404, мы перехватываем его нашим хэндлером.

    return HttpResponse(f'<h1>Архив по годам</h1><p>year: {year}</p>')


def page_not_found(request, exception):
    """
    Функция представления служит для отображения нужной нам страницы при 404 ошибке.

    :param request: HttpRequest - запрос от пользователя.
    :param exception: HttpRequest - 404 ошибка пользователя.
    :return: HttpResponseNotFound - сообщение об ошибке.
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
