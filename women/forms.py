from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband


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
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    """
    Класс описывает формы добавления статьи в модель Women.

    Атрибуты:\n
    title - обязательное текстовое поле заголовка минимальной длины 5 символов и максимальной длины 255 символов, также
    поле дополнительно содержит кастомные сообщения об ошибках;\n
    slug - обязательное уникальное индексируемое поле минимальной длины 5 символов и максимальной длины 100 символов -
    уникальный идентификатор записи;\n
    content - необязательное (required=False) текстовое поле c содержимым статьи;\n
    is_published - необязательное поле показывает, опубликована ли статья;\n
    cat - обязательное поле - категория поста;\n
    husband - необязательное поле, определяющее наличие мужа.
    """
    title = forms.CharField(error_messages={
        'min_length': 'Слишком короткий заголовок',
        'required': 'Без заголовка никак',
    },
        validators=[
            RussianValidator(),
        ],
        min_length=5, max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}), label='Заголовок')
    slug = forms.SlugField(max_length=255, label='URL', validators=[
        MinLengthValidator(5, message='Минимум 5 символов'),
        MaxLengthValidator(100, message='Максимум 100 символов'),
    ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, initial=True, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не замужем', label='Муж')

    def clean_content(self):
        """
        Метод-валидатор предназначен для отлова недопустимых символов. По факту является заменой класса RussianValidator,
        который следует использовать только в случае, если валидатор нужен часто. Если данная проверка является единичным
        случаем, то следует использовать функцию с синтаксисом: clean_<название поля>.

        :raises ValidatorError: Сообщение об ошибке.
        """
        content = self.cleaned_data['content']
        allowed_chars = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя- '

        if not (set(content) <= set(allowed_chars)):
            raise ValidationError('Должны присутствовать только русские символы, дефис и пробел.')
