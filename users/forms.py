from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    """
    Класс отвечает за авторизацию и аутентификацию пользователя.

    Атрибуты:\n
    username - логин пользователя;\n
    password - пароль пользователя.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}), label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Пароль')
    class Meta:
        """
        Вложенный класс предназначен для корректной обработки данных.

        Атрибуты:\n
        model - текущая модель пользователя;\n
        fields - поля, которые требуется отображать.
        """
        model = get_user_model()
        fields = ('username', 'password')