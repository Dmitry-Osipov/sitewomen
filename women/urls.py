from django.urls import path, re_path, register_converter

from .views import *
from .converters import *

# Все маршруты, которые относятся к приложению women, отдельно вынесены в этот файл.

register_converter(FourDigitYearConverter, 'year4')  # Регистрируем созданный конвертер. Первый аргумент -
# сам конвертер, второй аргумент - имя конвертера для urlpatterns.

urlpatterns = [  # В этой коллекции можно прописать сколько угодно маршрутов для страниц отображения клиенту.
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('addpage/', add_page, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<int:post_id>', show_post, name='post'),
    path('category:<int:cat_id>', show_category, name='category'),
    # Ниже используются пути и функции для представления базовых возможностей Django.
    path('cats/<int:cat_id>/', categories, name='cats_id'),  # По стандартам отрасли следует прописывать слэш в конце суффикса,
    # ибо если этого не сделать, то вместо привычного 127.0.0.1:8000/cats/ нужно будет писать 127.0.0.1:8000/cats, что неудобно.
    path('cats/<slug:cat_slug>/', categories_by_slug, name='cats'),  # Django проверяет маршруты в порядке их записи,
    # так что int следует ставить раньше, нежели slug, иначе отработает slug.
    # re_path(r'^archive/(?P<year>[0-9]{4})', archive),  # Функция позволяет делать то же самое, что и path, но с
    # использованием регулярных выражений. Полезно, если стандартных конвертеров недостаточно. Но это не лучшее решение,
    # ибо программист не сразу сможет понять, что мы тут обрабатываем, следует использовать отдельный класс в отдельном
    # файле и импортировать этот класс, переписав функцию на классическую path:
    path('archive/<year4:year>/', archive, name='archive'),
    path('main_filters/', main_filters, name='main_filters'),
]