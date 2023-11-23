from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import LoginUserForm


# Create your views here.
def login_user(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Функция представления служит для авторизации пользователя. В случае успешной авторизации происходит перенаправление
    на главную страницу.

    :param request: Запрос клиента.
    :return: Страница авторизации или главная страница.
    """
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = LoginUserForm()

    return render(request, 'users/login.html', context={'form': form})


def logout_user(request: HttpRequest) -> HttpResponseRedirect:
    """
    Функция представления служит для выхода пользователя.

    :param request: Запрос клиента.
    :return: Перенаправление на страницу авторизации.
    """
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
