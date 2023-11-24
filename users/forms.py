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


class RegisterUserForm(forms.ModelForm):
    """
    Класс отвечает за регистрацию пользователя.

    Атрибуты:\n
    username - логин пользователя;\n
    password - пароль пользователя;\n
    password2 - повтор пароля.
    """
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повтор пароля')

    class Meta:
        """
        Вложенный класс предназначен для корректной обработки данных.

        Атрибуты:\n
        model - текущая модель пользователя;\n
        fields - поля, которые требуется отображать;\n
        labels - метки для полей.
        """
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_password2(self) -> forms.CharField:
        """
        Метод-валидатор проверяет совпадение паролей.

        :return: Пароль.
        :raises ValidationError: Ошибка несовпадения паролей.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')

        return cd['password']

    def clean_email(self) -> forms.EmailField:
        """
        Метод-валидатор проверяет уникальность электронной почты.


        :return: Почта.
        :raises ValidationError: Ошибка наличия почты в БД.
        """
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')

        return email
