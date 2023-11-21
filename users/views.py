from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def login_user(request: HttpRequest) -> HttpResponse:
    """
    Функция представления служит для регистрации пользователя.

    :param request: Запрос клиента.
    :return: Заглушка.
    """
    return HttpResponse('login')


def logout_user(request: HttpRequest) -> HttpResponse:
    """
    Функция представления служит для выхода пользователя.

    :param request: Запрос клиента.
    :return: Заглушка.
    """
    return HttpResponse('logout')
