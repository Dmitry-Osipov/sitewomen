from django import template
from ..views import *

register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_categories(cat_selected: int = 0) -> dict[str, Category | int]:
    """
    Функция предназначена для возврата категорий постов. Используем включающий тег. Является предпочтительным вариантом
    в силу большего функционала и простоты записи в базовом шаблоне, однако требует создания дополнительного HTML-файла.

    :param cat_selected: id выбранной категории. По умолчанию 0 - не выбрана ни одна категория.
    :return: словарь содержит все категории с id и названиями. P.s.: этот словарь будет передаваться в шаблон,
    который мы указали аргументом в декораторе.
    """
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}


# Функция ниже является примером формирования простого тэга:
# @register.simple_tag(name='getcats')
# def get_categories():
#     """
#     Функция предназначена для возврата категорий постов. Используем простой тег. Требует следующего синтаксиса в шаблоне:
#     {%  getcats as categories %}
#     {% for cat in categories %}
#         <li><a href="{% url 'category' cat.id %}">{{ cat.name }}</a></li>
#     {% endfor %}
#
#     :return: list - список, состоящий из словарей, содержит все категории с id и названиями.
#     """
#     return cats_db
