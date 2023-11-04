from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

# Опишем главное меню сайта с помощью списка:
menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

class MyClass:
    """
    Тестовый класс. Нужен, чтобы проверить отработку шаблонизатора на собственном классе.
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b


# Create your views here.
def index(request):
    """
    Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/.

    :param request: HttpRequest - специальный класс, который содержит информацию о запросе. Через эту переменную нам
    доступна вся информация о запросе.
    :return: HttpResponse - экземпляр класса, который автоматически формирует нужный заголовок ответа (содержимое ответа
    передаётся строкой аргументом).
    """
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'float': 28.56,
        'lst': [1, 2, 'abc', True],
        'set': {1, 2, 3, 2, 5},
        'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
        'obj': MyClass(10, 20),
    }  # Словарь нужен, чтобы отработали переменные в шаблоне. Переменная в шаблоне - это ключ в словаре внутри функции
    # представления, по которому будет подставлено значение из словаря.

    # Простейший пример отдачи шаблона клиенту:
    # t = render_to_string('women/index.html')  # Переменная представляет текстовый вариант шаблона index.html. Прописываем
    # только имя, ибо директория templates находится в одном пакете. Дополнительно не нужно указывать приложение women и
    # директорию templates. Для избежания коллизий в директории templates создадим ещё одну директорию с именем приложения.
    # return HttpResponse(t)
    # Урежем код с функцией render.
    return render(request, 'women/index.html', context=data)


def about(request):
    """
    Функция представления служит для отображения страницы о сайте.

    :param request: HttpRequest - запрос пользователя.
    :return: HttpResponse - HTML-страница с заголовком первого уровня. Информационная страница о сайте.
    """
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'women/about.html', context=data)


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
    :raises Http404: Http404 - Ошибка 404 на сайте, если год меньше 1000 или больше 9999.
    """
    if year > 2023:
        uri = reverse('cats', args=(year, ))  # uri возвращает нам готовый маршрут, который мы подставляем
        # в redirect.
        # return redirect(uri, permanent=True)  # По умолчанию код перенаправления 302. Можно передать конкретный
        # URL, функцию представления или же имя маршрута, что и является рекомендуемой практикой, ибо это не хардкодинг
        # (имя перед этим следует прописать в urls.py).
        return HttpResponseRedirect(uri)  # Для редиректа с кодом 301 требуется возвращать класс HttpResponsePermanentRedirect.

    return HttpResponse(f'<h1>Архив по годам</h1><p>year: {year}</p>')


def page_not_found(request, exception):
    """
    Функция представления служит для отображения нужной нам страницы при 404 ошибке.

    :param request: HttpRequest - запрос от пользователя.
    :param exception: HttpRequest - 404 ошибка пользователя.
    :return: HttpResponseNotFound - сообщение об ошибке.
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
