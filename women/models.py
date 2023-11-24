from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


# Create your models here.
class PublishedManager(models.Manager):
    """
    Класс описывает менеджер моделей. Через него модель будет возвращать только опубликованные статьи.\n
    Т.е. доступ к возвращаемому параметру будет доступен в конкретной модели с синтаксисом:\n
    <название модели>.<переменная менеджера в модели>.<метод>\n
    Пример:\n
    Women.published.all()
    """
    def get_queryset(self) -> models.QuerySet:
        """
        Метод возвращает опубликованные статьи.

        :return: QuerySet - коллекция содержит только те записи, у которых флаг публикации = True.
        """
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


def translit_to_eng(s: str) -> str:
    """
    Вспомогательный метод для функции slugify преобразует кириллицу в латиницу с нижним регистром.

    :param s: Начальная строка на кириллице.
    :return: Новая строка в нижнем регистре на латинице.
    """
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}

    return ''.join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class Women(models.Model):
    """
    Класс является связкой для ORM с одноимённой таблицей в БД. Наследование от Model делает наш класс классом модели.

    Атрибуты:\n
    id - PRIMARY KEY, INTEGER, AUTOINCREMENT - главный ключ, формируется автоматически;\n
    title - VARCHAR - обязательное текстовое поле (содержит одну сроку) заголовка (имя женщины), максимальная длина -
    255 символов;\n
    slug - SLUG - обязательное уникальное (unique=True) индексируемое (db_index=True, нужно, чтобы был более быстрый
    выбор статей из БД) поле минимальной длины 5 символов и максимальной длины 100 символов - уникальный идентификатор
    записи;\n
    photo - VARCHAR - необязательное поле, по умолчанию NULL, - фото известной женщины, находящееся в директории по году,
    месяцу и дате добавления;\n
    content - TEXT - необязательное (blank=True) текстовое поле (содержит целое текстовое поле) c содержимым статьи;\n
    time_create - DATETIME - обязательное поле, содержащее время добавления записи в БД, во время первого появления
    конкретной записи автоматически проставляет время (auto_now_add=True);\n
    time_update - DATETIME - обязательное поле, содержащее время обновление записи в БД, автоматически обновляет время
    изменения конкретной записи в БД (auto_now=True);\n
    is_published - BOOLEAN - обязательное поле показывает, опубликована ли статья, по умолчанию все статьи не
    публикуются;\n
    cat - FOREIGN KEY - обязательное поле, запрещает удалять категории, которые связаны с постами, имеет название
    менеджера записей "posts", - внешний ключ таблицы категорий - в БД будет cat_id - "_id" Django добавляет
    самостоятельно. Причём при запросе в ORM cat - выдаст название категории, а при запросе cat_id - выдаст id категории.
    Т.е. cat - это полноценный объект (имеет name и slug), а cat_id - просто int;\n
    tags - MANY TO MANY - необязательное поле имеет название менеджера записей "tags", - внешний ключ таблицы тегов
    (связь многое-ко-многому);\n
    husband - ONE TO ONE - необязательное поле, имеющее название менеджера записей "wuman", по умолчанию ставится NULL -
    внешний ключ таблицы мужа (связь один-к-одному);\n
    objects - стандартный менеджер модели - при добавлении собственного менеджера, атрибут objects автоматически
    затирается, так что следует прописать его явно;\n
    published - кастомный менеджер модели;\n
    author - FOREIGN KEY - обязательное поле, при удалении поста выставляет в таблице значение на NULL, по умолчанию NULL,
    название менеджера записей "posts" - внешний ключ таблицы авторов постов.
    """
    class Status(models.IntegerChoices):
        """
        Вложенный класс перечисления предназначен для определения осмысленных имён значений, содержащихся в коллекции
        класса choices. Т.е. список choices будет состоять из кортежей, которые содержат значение (int) + метка для
        пользователя (str).

        Атрибуты:\n
        DRAFT и PUBLISHED - tuple - кортеж, состоящие из двух элементов: первое значение (int) – это то, которое
        записывается в БД, а второе (str) – это его имя (метка). Фигурируют в коллекции choices (list). DRAFT - константа
        для 0 (False) - черновик. PUBLISHED - константа для 1 (True) - Опубликовано.
        """
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок', validators=[])
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug',
                            validators=[
        MinLengthValidator(5, message='Минимум 5 символов'),
        MaxLengthValidator(100, message='Максимум 100 символов'),
                                        ]
                            )
    photo = models.ImageField(upload_to='photos/%Y-%m-%d', default=None, null=True, blank=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Тег')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='woman', verbose_name='Муж')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        """
        Вложенный класс предназначен для фильтрации и корректной обработки данных.

        Атрибуты:\n
        verbose_name - str - меняет название ссылки таблицы модели в админ-панели (единственное число);\n
        verbose_name_plural - str - меняет название ссылки таблицы модели в админ-панели (множественное число);\n
        ordering - list - определяет порядок сортировки выбранных записей модели;\n
        indexes - list - определяет столбцы, записи которых должны быть пронумерованы, что позволит ускорить сортировку.
        """
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self) -> models.CharField:
        """
        Метод служит для корректного отображения записи из БД.

        :return: Имя женщины.
        """
        return self.title

    def get_absolute_url(self):
        """
        Метод формирует URL-адрес для каждой конкретной записи.

        :return: URL-адрес конкретной записи.
        """
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs) -> None:
    #     """
    #     Метод создаёт слаг на основе заголовка статьи и сохраняет запись в БД.
    #     """
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)


class Category(models.Model):
    """
    Класс является связкой для ORM - создаёт таблицу категорий.

    Атрибуты:\n
    name - VARCHAR - обязательное индексируемое поле максимальной длины 100 символов - название категории;\n
    slug - SLUG - обязательное уникальное индексируемое поле максимальной длины 255 символов - уникальный идентификатор
    записи.
    """
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    class Meta:
        """
        Вложенный класс предназначен для фильтрации и корректной обработки данных.

        Атрибуты:\n
        verbose_name - str - меняет название ссылки таблицы модели в админ-панели (единственное число);\n
        verbose_name_plural - str - меняет название ссылки таблицы модели в админ-панели (множественное число).
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> models.CharField:
        """
        Метод служит для корректного отображения записи из БД.

        :return: Название категории.
        """
        return self.name

    def get_absolute_url(self):
        """
        Метод формирует URL-адрес для каждой конкретной записи.

        :return: URL-адрес конкретной записи.
        """
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    """
    Класс модели для тегов.

    Атрибуты:\n
    tag - VARCHAR - обязательное индексируемое текстовое поле длиной 100 символов - тег записи;\n
    slug - SLUG - обязательное индексируемое уникальное поле длиной 255 символов - слаг индекса.
    """
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> models.CharField:
        """
        Метод служит для корректного отображения записи из БД.

        :return: Тег записи.
        """
        return self.tag

    def get_absolute_url(self):
        """
        Метод формирует URL-адрес для каждой конкретной записи.

        :return: URL-адрес конкретной записи.
        """
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    """
    Класс модели мужа известной женщины.

    Атрибуты:\n
    name - VARCHAR - обязательное поле максимальной длины 100 символов - имя мужа;\n
    age - INTEGER - обязательное поле, может иметь значение NULL - возраст мужа;\n
    m_count - INTEGER - необязательное поле по умолчанию 0 - количество свадеб мужа.
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self) -> models.CharField:
        """
        Метод служит для корректного отображения записи из БД.

        :return: Имя мужа.
        """
        return self.name


class UploadFiles(models.Model):
    """
    Класс модели для загружаемых файлов в БД.

    Атрибуты:\n
    file - обязательное поле хранения файла (аргументом принимает директорию сохранения файла).
    """
    file = models.FileField(upload_to='uploads_model')
