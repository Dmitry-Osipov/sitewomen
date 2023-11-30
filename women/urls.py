from django.urls import path, register_converter

from .converters import *
from .views import *

# Все маршруты, которые относятся к приложению women, отдельно вынесены в этот файл.

register_converter(FourDigitYearConverter, 'year4')  # Регистрируем созданный конвертер. Первый аргумент -
# сам конвертер, второй аргумент - имя конвертера для urlpatterns.

urlpatterns = [  # В этой коллекции можно прописать сколько угодно маршрутов для страниц отображения клиенту.
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', UpdatePage.as_view(), name='edit_page'),

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