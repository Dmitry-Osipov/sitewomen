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
    def get_queryset(self):
        """
        Метод возвращает опубликованные статьи.

        :return: QuerySet - коллекция содержит только те записи, у которых флаг публикации = True.
        """
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    """
    Класс является связкой для ORM с одноимённой таблицей в БД. Наследование от Model делает наш класс классом модели.

    Атрибуты:\n
    id - PRIMARY KEY, INTEGER, AUTOINCREMENT - главный ключ, формируется автоматически;\n
    title - VARCHAR - обязательное текстовое поле (содержит одну сроку) заголовка (имя женщины), максимальная длина -
    255 символов;\n
    slug - SLUG - обязательное уникальное (unique=True) индексируемое (db_index=True, нужно, чтобы был более быстрый
    выбор статей из БД) поле максимальной длины 255 символов - уникальный идентификатор записи;\n
    content - TEXT - необязательное (blank=True) текстовое поле (содержит целое текстовое поле) c содержимым статьи;\n
    time_create - DATETIME - обязательное поле, содержащее время добавления записи в БД, во время первого появления
    конкретной записи автоматически проставляет время (auto_now_add=True);\n
    time_update - DATETIME - обязательное поле, содержащее время обновление записи в БД, автоматически обновляет время
    изменения конкретной записи в БД (auto_now=True);\n
    is_published - BOOLEAN - обязательное поле показывает, опубликована ли статья, по умолчанию все статьи не
    публикуются;\n
    cat - FOREIGN KEY - обязательное поле, запрещает удалять категории, которые связаны с постами - внешний ключ таблицы
    категорий - в БД будет cat_id - "_id" Django добавляет самостоятельно. Причём при запросе в ORM cat - выдаст название
    категории, а при запросе cat_id - выдаст id категории. Т.е. cat - это полноценный объект (имеет name и slug), а
    cat_id - просто int;\n
    objects - стандартный менеджер модели - при добавлении собственного менеджера, атрибут objects автоматически
    затирается, так что следует прописать его явно;\n
    published - кастомный менеджер модели.
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

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        """
        Вложенный класс предназначен для фильтрации данных.

        Атрибуты:\n
        ordering - list - определяет порядок сортировки выбранных записей модели;\n
        indexes - list - определяет столбцы, записи которых должны быть пронумерованы, что позволит ускорить сортировку.
        """
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]

    def __str__(self):
        """
        Метод служит для корректного отображения записи из БД.

        :return: str - имя актрисы.
        """
        return self.title

    def get_absolute_url(self):
        """
        Метод формирует URL-адрес для каждой конкретной записи.

        :return: str - URL-адрес конкретной записи.
        """
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    """
    Класс является связкой для ORM - создаёт таблицу категорий.

    Атрибуты:\n
    name - VARCHAR - обязательное индексируемое поле максимальной длины 100 символов - название категории;\n
    slug - SLUG - обязательное уникальное индексируемое поле максимальной длины 255 символов - уникальный идентификатор
    записи.
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        """
        Метод служит для корректного отображения записи из БД.

        :return: str - название категории.
        """
        return self.name
