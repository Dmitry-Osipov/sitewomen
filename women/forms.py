from django import forms
from .models import Category, Husband


class AddPostForm(forms.Form):
    """
    Класс описывает формы добавления статьи в модель Women.

    Атрибуты:\n
    title - обязательное текстовое поле заголовка максимальной длины - 255 символов;\n
    slug - обязательное уникальное индексируемое поле максимальной длины 255 символов - уникальный идентификатор записи;\n
    content - необязательное (required=False) текстовое поле c содержимым статьи;\n
    is_published - необязательное поле показывает, опубликована ли статья;\n
    cat - обязательное поле - категория поста;\n
    husband - необязательное поле, определяющее наличие мужа.
    """
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}), label='Заголовок')
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, initial=True, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категория')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не замужем', label='Муж')
