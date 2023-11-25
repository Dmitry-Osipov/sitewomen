from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


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


class RegisterUserForm(UserCreationForm):
    """
    Класс отвечает за регистрацию пользователя.

    Атрибуты:\n
    username - логин пользователя;\n
    password1 - пароль пользователя;\n
    password2 - повтор пароля.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}), label='Логин')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Повтор пароля')

    class Meta:
        """
        Вложенный класс предназначен для корректной обработки данных.

        Атрибуты:\n
        model - текущая модель пользователя;\n
        fields - поля, которые требуется отображать;\n
        labels - метки для полей;\n
        widgets - CSS-виджеты полей.
        """
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

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


class ProfileUserForm(forms.ModelForm):
    """
    Класс формы предназначен для создания профиля пользователя.

    Атрибуты:\n
    username - логин пользователя, запрещено для изменения (disabled=True);\n
    email - почта пользователя, запрещена для изменений.
    """
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-input'}), label='Логин')
    email = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-input'}), label='E-mail')

    class Meta:
        """
        Вложенный класс предназначен для корректной обработки данных.

        Атрибуты:\n
        model - текущая модель пользователя;\n
        fields - поля, которые требуется отображать;\n
        labels - метки для полей;\n
        widgets - CSS-виджеты полей.
        """
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Класс формы для смены пароля пользователя.

    Атрибуты:\n
    old_password - старый пароль;\n
    new_password1 - новый пароль;\n
    new_password2 - повтор нового пароля.
    """
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Старый пароль')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Новый пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), label='Подтверждение пароля')
