from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import *


# Create your views here.
class LoginUser(LoginView):
    """
    Класс представления служит для авторизации пользователя.

    Атрибуты:\n
    form_class - forms.AuthenticationForm - класс формы аутентификации пользователя;\n
    template_name - str - имя HTML-шаблона;\n
    extra_context - dict - дополнительный словарь контекста.
    """
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     """
    #     Метод отвечает за перенаправление клиента на определённую страницу при авторизации. Имеет наивысший приоритет
    #     перенаправления клиента.
    #
    #     :return: Ленивое перенаправление на главную страницу.
    #     """
    #     return reverse_lazy('home')


class RegisterUser(CreateView):
    """
    Класс представления отвечает за регистрацию нового пользователя.

    Атрибуты:\n
    form_class - forms.UserCreationForm - класс формы;\n
    template_name - str - HTML-шаблон;\n
    extra_context - dict - дополнительные данные;\n
    success_url - Callable - переход на страницу после успешной регистрации.
    """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    """
    Класс представления отвечает за отображение профиля пользователя.

    Атрибуты:\n
    model - models.Model - модель;\n
    form_class - forms.ModelForm - класс формы;\n
    template_name - str - HTML-шаблон;\n
    extra_context - dict - дополнительные данные.
    """
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        """
        Метод отвечает за перенаправление клиента на определённую страницу при изменении и сохранении каких-либо полей
        профиля. Имеет наивысший приоритет перенаправления клиента.

        :return: Ленивое перенаправление на страницу профиля.
        """
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Метод отбирает ту запись, которая будет отображаться и редактироваться.

        :return: Текущий пользователь.
        """
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """
    Класс представления служит для отображения страницы смены пароля пользователя.
    """
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Смена пароля'}


# Функции представления, заменённые на классы представления:
# def login_user(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
#     """
#     Функция представления служит для авторизации пользователя. В случае успешной авторизации происходит перенаправление
#     на главную страницу.
#
#     :param request: Запрос клиента.
#     :return: Страница авторизации или главная страница.
#     """
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#
#     return render(request, 'users/login.html', context={'form': form})
#
#
# def logout_user(request: HttpRequest) -> HttpResponseRedirect:
#     """
#     Функция представления служит для выхода пользователя.
#
#     :param request: Запрос клиента.
#     :return: Перенаправление на страницу авторизации.
#     """
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))
#
#
# def register(request: HttpRequest) -> HttpResponse:
#     """
#     Функция представления отвечает за регистрацию нового пользователя.
#
#     :param request: Запрос клиента.
#     :return: Страница регистрации клиента.
#     """
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#
#     return render(request, 'users/register.html', context={'form': form})