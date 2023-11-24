from django.contrib.auth.views import LoginView

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