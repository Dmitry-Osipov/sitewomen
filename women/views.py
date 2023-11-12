from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse

from .models import *

# Опишем главное меню сайта с помощью списка из словарей с маршрутом к соответствующей странице:
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
]


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/.

    :param request: Специальный класс, который содержит информацию о запросе. Через эту переменную нам
    доступна вся информация о запросе.
    :return: Экземпляр класса, который автоматически формирует нужный заголовок ответа (содержимое ответа
    передаётся строкой аргументом).
    """
    posts = Women.published.all().select_related('cat')

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }

    return render(request, 'women/index.html', context=data)


def about(request: HttpRequest) -> HttpResponse:
    """
    Функция представления служит для отображения страницы о сайте.

    :param request: Запрос пользователя.
    :return: HTML-страница с заголовком первого уровня. Информационная страница о сайте.
    """
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'women/about.html', context=data)


def show_post(request: HttpRequest, post_slug: models.SlugField) -> HttpResponse:
    """
    Функция представления служит для отображения конкретного поста о женщине.

    :param request: Запрос пользователя.
    :param post_slug: Уникальный идентификатор записи.
    :return: Запись из БД про известную женщину.
    :raises Http404: Ошибка 404 на сайте, если статья с нужным слагом не была найдена в БД.
    """
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', context=data)


def show_category(request: HttpRequest, cat_slug: models.SlugField) -> HttpResponse:
    """
    Функция представления отвечает за отображение выбранной категории.

    :param request: Запрос пользователя.
    :param cat_slug: Уникальный идентификатор категории.
    :return: Страница со всеми постами подходящей категории.
    :raises Http404: Ошибка 404 на сайте, если категория с нужным слагом не была найдена в БД.
    """
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'women/index.html', context=data)


def add_page(request: HttpRequest) -> HttpResponse:
    """
    Функция представления служит для добавления статьи про известную женщину.

    :param request: Запрос пользователя.
    :return: Текст про добавление статьи.
    """
    return HttpResponse('Добавление статьи')


def contact(request: HttpRequest) -> HttpResponse:
    """
    Функция представления служит для обратной связи разработчику сайта.

    :param request: Запрос пользователя.
    :return: Текст про обратную связь.
    """
    return HttpResponse('Обратная связь')


def login(request: HttpRequest) -> HttpResponse:
    """
    Функция представления служит для авторизации пользователя на сайте.

    :param request: Запрос пользователя.
    :return: Текст про авторизацию.
    """
    return HttpResponse('Авторизация')


def show_tag_postlist(request: HttpRequest, tag_slug: models.SlugField) -> HttpResponse:
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)


def page_not_found(request: HttpRequest, exception: Http404) -> HttpResponseNotFound:
    """
    Функция представления служит для отображения нужной нам страницы при 404 ошибке.

    :param request: Запрос от пользователя.
    :param exception: 404 ошибка пользователя.
    :return: Страница с сообщением об ошибке.
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# Все функции представления ниже нужны только для отображения базовых возможностей Django.
def categories(request, cat_id):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/cat/<число>/.

    :param request: HttpRequest - запрос пользователя.
    :param cat_id: int - Уникальный идентификатор записи.
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Пользователь получает число, которое вводит в
    запросе. Прим.: HTML-теги не экранируются.
    """
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/cat/<слаг>/.

    :param request: HttpRequest - запрос пользователя.
    :param cat_slug: str - Уникальный идентификатор записи.
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Пользователь получает слаг, который вводит в
    запросе.
    """
    if request.GET:  # Словарь GET содержит параметры запроса в формате ключ=значение.
        print(request.GET)  # <QueryDict: {'name': ['gagarina'], 'type': ['pop']}>
        # <QueryDict: {'name': ['gagarina'], 'type': ['pop']}>
        lst = [f"{key}={val}" for key, val in request.GET.items()]
        print('|'.join(lst))  # name=gagarina|type=pop
    if request.POST:  # Словарь POST содержит параметры передачи в том же самом классе.
        print(request.POST)
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')


def archive(request, year):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/archive/<год>/.

    :param request: HttpRequest - запрос пользователя.
    :param year: int - год, принадлежащий промежутку [1000;9999].
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Пользователь получает год, который вводит в
    запросе. Либо HttpResponseRedirect - перенаправление на страницу категорий, если год больше 2023 и меньше 9999.
    :raises Http404: ошибка 404 на сайте, если год меньше 1000 или больше 9999.
    """
    if year > 2023:
        uri = reverse('cats', args=(year, ))  # uri возвращает нам готовый маршрут, который мы подставляем
        # в redirect.
        # return redirect(uri, permanent=True)  # По умолчанию код перенаправления 302. Можно передать конкретный
        # URL, функцию представления или же имя маршрута, что и является рекомендуемой практикой, ибо это не хардкодинг
        # (имя перед этим следует прописать в urls.py).
        return HttpResponseRedirect(uri)  # Для редиректа с кодом 301 требуется возвращать класс HttpResponsePermanentRedirect.

    return HttpResponse(f'<h1>Архив по годам</h1><p>year: {year}</p>')


class MyClass:
    """
    Тестовый класс. Нужен, чтобы проверить отработку шаблонизатора на собственном классе.
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b


data_db = [  # Имитируем набор записей из БД списком из словарей.
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджели́на Джоли́</h1> (англ. Angelina Jolie[5], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
    Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая награду) и двух «Премий Гильдии киноактёров США».
    Дебютировала в кино в 1982 году, сыграв роль в комедийном фильме «В поисках выхода» (где снимались также её отец и мать)[6], однако известность получила после того, как сыграла героиню видеоигр Лару Крофт в фильмах «Лара Крофт: Расхитительница гробниц» и «Лара Крофт: Расхитительница гробниц 2 — Колыбель жизни».
    В 2009, 2011 и 2013 годах по версии журнала Forbes Джоли была названа самой высокооплачиваемой актрисой Голливуда[7][8].
    Её наиболее успешными с коммерческой стороны фильмами стали «Малефисента» (сборы в мировом прокате — 758 миллионов долларов США), «Мистер и миссис Смит» (сборы в мировом прокате — 478 миллионов), «Особо опасен» (341 миллион), «Солт» (293 миллиона ), а также «Турист» (278 миллионов), «Лара Крофт: Расхитительница гробниц» (274 миллиона) и картина с участием Николаса Кейджа «Угнать за 60 секунд» (237 миллионов долларов США)[9].''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]


def main_filters(request):
    """
    Функция представления отвечает за демонстрацию основных фильтров шаблонизатора Django.

    :param request: HttpRequest - запрос пользователя.
    :return: HttpResponse - HTML-страница с примерами работы различных стандартных фильтров шаблонизатора.
    """
    data = {
        'title': 'Страница о фильтрах',
        'menu': menu,
        'float': 28.56,
        'lst': [1, 2, 'abc', True],
        'set': {1, 2, 3, 2, 5},
        'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
        'obj': MyClass(10, 20),
        'some_title': '',
        'url': slugify('The Main Page'),
        'posts': data_db,
    }  # Словарь нужен, чтобы отработали переменные в шаблоне. Переменная в шаблоне - это ключ в словаре внутри функции
    # представления, по которому будет подставлено значение из словаря.

    # Простейший пример отдачи шаблона клиенту:
    # t = render_to_string('women/index.html')  # Переменная представляет текстовый вариант шаблона index.html. Прописываем
    # только имя, ибо директория templates находится в одном пакете. Дополнительно не нужно указывать приложение women и
    # директорию templates. Для избежания коллизий в директории templates создадим ещё одну директорию с именем приложения.
    # return HttpResponse(t)
    # Урежем код с функцией render.
    return render(request, 'women/main_filters.html', context=data)
