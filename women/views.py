from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.core.cache import cache

from .forms import *
from .models import *
from .utils import DataMixin


# Create your views here.
class WomenHome(DataMixin, ListView):
    """
    Класс представления отвечает за отображение базовой страницы сайта.

    Атрибуты:\n
    model - models.Model - модель, из которой будет получен QuerySet;\n
    template_name - str - маршрут для отображения страницы;\n
    context_object_name - str - название переменной выборки из БД в HTML-шаблоне;\n
    title_page - str - заголовок страницы;\n
    cat_selected - int - рубрика поста.
    """
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        """
        Метод вызывает выборку всех опубликованных записей, которые содержат поле категории. Метод кэширует все записи
        на 60 секунд.

        :return: Коллекция отобранных записей.
        """
        w_lst = cache.get('women_posts')
        if not w_lst:
            w_lst = Women.published.all().select_related('cat')
            cache.set('women_posts', w_lst, 60)

        return w_lst


@login_required  # Дополнительно можно указать параметр login_url для изменения страницы перенаправления.
def about(request: HttpRequest) -> HttpResponse:
    """
    Функция представления служит для отображения страницы о сайте. Страница доступна только для авторизованных клиентов.

    :param request: Запрос пользователя.
    :return: Страница загрузки графического файла на машину.
    """
    contact_list = Women.published.all()  # Получаем список всех статей.
    paginator = Paginator(contact_list, 3)  # Создаём класс пагинации.
    page_number = request.GET.get('page')  # Получаем номер текущей страницы.
    page_obj = paginator.get_page(page_number)  # Получаем конкретную страницу.

    data = {
        'title': 'О сайте',
        'page_obj': page_obj,
    }

    return render(request, 'women/about.html', context=data)


class ShowPost(DataMixin, DetailView):
    """
    Класс представления отвечает за отображение конкретного поста.

    Атрибуты:\n
    template_name - str - маршрут для отображения страницы;\n
    slug_url_kwarg - str - переменная, которая фигурирует в URL-маршруте;\n
    context_object_name - str - название переменной выборки из БД в HTML-шаблоне;\n
    """
    # model = Women - атрибут не имеет смысла, т.к. модель уже участвует в выборке в методе get_object.
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # Если фигурирует pk, то переменная будет pk_url_kwarg.
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """
        Метод срабатывает в момент прихода GET-запроса. Является аналогом для атрибута extra_context, позволяя более
        тонко настроить работу с клиентом.

        :param kwargs: Контекст для отображения на странице (например, меню, заголовок и т.п.)
        :return: Контекст запроса.
        """
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        """
        Метод отображает только опубликованные записи. Для черновика вылетит ошибка 404.

        :param queryset: Выборка, по умолчанию никакой.
        :return: Опубликованную статью.
        :raises Http404: Ошибка 404.
        """
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    """
    Класс представления отвечает за отображение категорий на базовой странице сайта.

    Атрибуты:\n
    template_name - str - маршрут для отображения страницы;\n
    context_object_name - str - название переменной выборки из БД в HTML-шаблоне;\n
    allow_empty - bool - при пустом списке "posts" генерируется исключение 404.
    """
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        """
        Метод вызывает выборку записей по фильтру "slug" у категории.

        :return: Коллекция отобранных записей.
        """
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        """
        Метод срабатывает в момент прихода GET-запроса. Является аналогом для атрибута extra_context, позволяя более
        тонко настроить работу с клиентом.

        :param kwargs: Контекст для отображения на странице (например, меню, заголовок и т.п.)
        :return: Контекст запроса.
        """
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    """
    Класс представления служит для добавления статьи про известную женщину. Страница добавления статьи доступна только
    авторизованным пользователям.

    Атрибуты:\n
    form_class - forms.ModelForm - переменная ссылается на класс формы;\n
    template_name - str - маршрут для отображения страницы;\n
    success_url - Callable - полный маршрут страницы перенаправления (в случае успешной обработки формы);\n
    extra_context - dict - контекст для отображения на странице (например, меню, заголовок и т.п.);\n
    permission_required - str - разрешение на получение доступа к странице.
    """
    form_class = AddPostForm  # Можно указать аналог этого атрибута атрибутами ниже:
    # model = Women - model - models.Model - связанная модель.
    # fields = ('title', 'slug', 'content', 'is_published', 'cat') - tuple - поля, которые будут отображены в форме.
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # Если убрать атрибут, то URL будет браться из метода get_absolute_url связанной
    # модели.
    title_page = 'Добавление статьи'
    # login_url = 'home' - страница перенаправления для неавторизованных пользователей.
    permission_required = 'women.add_women'  # Синтаксис: <приложение>.<действие>_<таблица>.

    def form_valid(self, form: forms.ModelForm) -> HttpResponseRedirect:
        """
        Метод автоматически присваивает id автора к добавляемой записи с переходом на главную страницу.

        :param form: Проверенная и заполненная форма добавления новой статьи.
        :return: Заполненная форма.
        """
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    """
    Класс представления служит для обновления статьи про известную женщину.

    Атрибуты:\n
    model - model - models.Model - связанная модель;\n
    fields - tuple - поля, которые будут отображены в форме;\n
    template_name - str - маршрут для отображения страницы;\n
    success_url - Callable - полный маршрут страницы перенаправления (в случае успешной обработки формы);\n
    extra_context - dict - контекст для отображения на странице (например, меню, заголовок и т.п.);\n
    permission_required - str - разрешение на получение доступа к странице.
    """
    model = Women
    fields = ('title', 'content', 'photo', 'is_published', 'cat')
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women'


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    """
    Класс представления служит для отображения страницы обратной связи.

    Атрибуты:\n
    form_class - forms.ModelForm - переменная ссылается на класс формы;\n
    template_name - str - маршрут для отображения страницы;\n
    success_url - Callable - полный маршрут страницы перенаправления (в случае успешной обработки формы);\n
    title_page - str - заголовок страницы.
    """
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    title_page = 'Обратная связь'

    def form_valid(self, form):
        """
        Метод выводит сообщение пользователя с переходом на главную страницу.

        :param form: Проверенная и заполненная форма добавления новой статьи.
        :return: Заполненная форма.
        """
        print(form.cleaned_data)
        return super().form_valid(form)


class TagPostList(DataMixin, ListView):
    """
    Класс представления отвечает за отображение тегов на базовой странице сайта.

    Атрибуты:\n
    template_name - str - маршрут для отображения страницы;\n
    context_object_name - str - название переменной выборки из БД в HTML-шаблоне;\n
    allow_empty - bool - при пустом списке "posts" генерируется исключение 404.
    """
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Метод срабатывает в момент прихода GET-запроса. Является аналогом для атрибута extra_context, позволяя более
        тонко настроить работу с клиентом.

        :param kwargs: Контекст для отображения на странице (например, меню, заголовок и т.п.).
        :return: Контекст запроса.
        """
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        """
        Метод вызывает выборку записей по фильтру "slug" у тега.

        :return: Коллекция отобранных записей.
        """
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request: HttpRequest, exception: Http404) -> HttpResponseNotFound:
    """
    Функция представления служит для отображения нужной нам страницы при 404 ошибке.

    :param request: Запрос от пользователя.
    :param exception: 404 ошибка пользователя.
    :return: Страница с сообщением об ошибке.
    """
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# Функции представления, замененные классами представления. По количеству лишнего кода чётко видны преимущества классов:
# def index(request: HttpRequest) -> HttpResponse:
#     """
#     Функция представления, которая отвечает за отображение HTML-страницы в браузере по адресу 127.0.0.1:8000/.
#
#     :param request: Специальный класс, который содержит информацию о запросе. Через эту переменную нам
#     доступна вся информация о запросе.
#     :return: Экземпляр класса, который автоматически формирует нужный заголовок ответа (содержимое ответа
#     передаётся строкой аргументом).
#     """
#     posts = Women.published.all().select_related('cat')
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=data)
#
#
# def add_page(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
#     """
#     Функция представления служит для добавления статьи про известную женщину.
#
#     :param request: Запрос пользователя.
#     :return: Форма добавления статьи. Если статья добавлена в БД, происходит перенаправление на главную страницу сайта.
#     """
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form,
#     }
#
#     return render(request, 'women/addpage.html', context=data)
#
#
# def show_category(request: HttpRequest, cat_slug: models.SlugField) -> HttpResponse:
#     """
#     Функция представления отвечает за отображение выбранной категории.
#
#     :param request: Запрос пользователя.
#     :param cat_slug: Уникальный идентификатор категории.
#     :return: Страница со всеми постами подходящей категории.
#     :raises Http404: Ошибка 404 на сайте, если категория с нужным слагом не была найдена в БД.
#     """
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#
#     return render(request, 'women/index.html', context=data)
#
#
# def show_tag_postlist(request: HttpRequest, tag_slug: models.SlugField) -> HttpResponse:
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)
#
#
# def show_post(request: HttpRequest, post_slug: models.SlugField) -> HttpResponse:
#     """
#     Функция представления служит для отображения конкретного поста о женщине.
#
#     :param request: Запрос пользователя.
#     :param post_slug: Уникальный идентификатор записи.
#     :return: Запись из БД про известную женщину.
#     :raises Http404: Ошибка 404 на сайте, если статья с нужным слагом не была найдена в БД.
#     """
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'women/post.html', context=data)
#
#
# @permission_required(perm='women.view_women', raise_exception=True)
# def contact(request: HttpRequest) -> HttpResponse:
#     """
#     Функция представления служит для обратной связи разработчику сайта.
#
#     :param request: Запрос пользователя.
#     :return: Текст про обратную связь.
#     """
#     return HttpResponse('Обратная связь')


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
    # Опишем главное меню сайта с помощью списка из словарей с маршрутом к соответствующей странице:
    menu = [
        {'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'},
    ]

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
