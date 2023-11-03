from django.http import HttpResponse
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
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')


def archive(request, year):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/cat/<слаг>/.

    :param request: HttpRequest - запрос пользователя.
    :param year: str - год, принадлежащий промежутку [1000;9999].
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Пользователь получает год, который вводит в
    запросе.
    """
    return HttpResponse(f'<h1>Архив по годам</h1><p>year: {year}</p>')
