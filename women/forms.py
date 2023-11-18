from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    """
    Класс-валидатор предназначен для отлова недопустимых символов.

    Атрибуты:\n
    ALLOWED_CHARS - str - допустимые символы слова;\n
    code - str - скоращённое название.
    """
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя- '
    code = 'russian'

    def __init__(self, message: str = None) -> None:
        """
        Иницализатор класса.

        :param message: Сообщение об ошибке
        """
        self.message = message if message else 'Должны присутствовать только русские символы, дефис и пробел.'

    def __call__(self, value, *args, **kwargs):
        """
        Метод срабатывает, когда валидатор вызывается. Внутри прописана проверка на недопустимые символы.

        :param value: Введённые данные.
        :raises ValidationError: Сообщение об ошибке.
        """
        if not all(char in self.ALLOWED_CHARS for char in value):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    """
    Класс описывает формы добавления статьи в модель Women.

    Атрибуты:\n
    cat - обязательное поле - категория поста;\n
    husband - необязательное поле, определяющее наличие мужа.
    """

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не замужем', label='Муж')

    class Meta:
        """
        Вложенный класс предназначен для упрощённой связи формы с моделью.

        Атрибуты:\n
        model - models.Model - описывает взаимосвязь формы (AddPostForm) с моделью (Women);\n
        fields - tuple - поля, которые будут отображаться в форме, по умолчанию все. Т.е. автоматически в форме появятся
        все поля из Women, кроме тех, что заполняются автоматически;\n
        widgets - dict - виджеты для определённых полей;\n
        labels - dict - даём нормальные наименования определённых полей для клиента.
        """
        model = Women
        fields = ('title', 'slug', 'content', 'is_published', 'cat', 'husband', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self) -> forms.CharField:
        """
        Метод-валидатор предназначен для отлова недопустимых заголовков. По факту является заменой класса
        RussianValidator, который следует использовать только в случае, если валидатор нужен часто. Если данная проверка
        является единичным случаем, то следует использовать функцию с синтаксисом: clean_<название поля>.

        :return: Заголовок.
        :raises ValidationError: Ошибка длины заголовка.
        """
        title = self.cleaned_data.get('title')
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов.')

        return title
