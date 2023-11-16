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
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)
    is_published = forms.BooleanField(required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False)
