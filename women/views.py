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


def categories(request):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/cat/.

    :param request: HttpRequest - запрос пользователя.
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Прим.: HTML-теги не экранируются.
    """
    return HttpResponse('<h1>Статьи по категориям</h1>')
