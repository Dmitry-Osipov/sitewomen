from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils.safestring import mark_safe, SafeString

from .models import Women, Category

# Register your models here.
class MarriedFilter(admin.SimpleListFilter):
    """
    Вспомогательный класс для WomenAdmin. Нужен для создания фильтра по связанной таблице husband класса Women. Фильтр
    будет отбирать замужних и незамужних женщин.

    Атрибуты:\n
    title - str - название фильтра;\n
    parameter_name - str - ключ для GET-запроса.
    """
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> list[tuple[str, str]]:
        """
        Метод нужен для настройки нового люкапа фильтрации.

        :param request: Запрос пользователя.
        :param model_admin: Класс отображения статей.
        :return: Значение параметра parameter_name + кликабельное название позиции для пользователя.
        """
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request: HttpRequest, queryset):
        """
        Метод возвращает отфильтрованные посты. По умолчанию возвращаются все посты.

        :param request: Запрос пользователя.
        :param queryset: Менеджер модели.
        :return: Отфильтрованный QuerySet по нужным значениям
        """
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)

        if self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)  # Регистрируем модель.
class WomenAdmin(admin.ModelAdmin):
    """
    Класс отвечает за настройку отображения отдельных статей.

    Атрибуты:\n
    fields - tuple - список полей, которые отображаются в форме изменения и добавления конкретного поста. Аналогом будет
    атрибут exclude - коллекция исключает поля;\n
    readonly_fields - tuple - список полей, доступных только для чтения. ВАЖНО: можно добавить только необязательные поля, иначе
    мы не сможем прописать их при добавлении статьи - приведёт к непредсказуемому поведению и ошибке в итоге. Либо можно
    обойти проблемы, например, функцией slugify (не поддерживает кириллицу).;\n
    prepopulated_fields - dict - словарь с полями, заполняющимися автоматически при добавлении новой записи;\n
    filter_horizontal - tuple - список значений внутри указанной коллекции будет доступен для более красивого и
    упрощённого добавления в БД;\n
    list_display - tuple - список полей, которые требуется отобразить;\n
    list_display_links - tuple - список полей, по которым можно перейти на конкретный пост;\n
    ordering - tuple - порядок сортировки (если указано 2 и более поля, то сначала будет сортироваться по первому полю,
    а затем, если будут совпадения, то по второму полю);\n
    list_editable - tuple - список полей, которые можно редактировать;\n
    list_per_page - int - максимальное количество отображаемых статей (пагинация реализуется автоматически);\n
    actions - tuple - список действий (посредством функций);\n
    search_fields - tuple - список полей, по которым будет осуществляться поиск статьи по символам;\n
    list_filter - tuple - список отвечает за специальный блок, в котором можно указать фильтрацию по указанным полям;\n
    save_on_top - bool - флаг действий сохранения и удаления на верхней части админ-панели.
    """
    fields = ('title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags')  # Аналог exclude - исключает выбранные поля.
    readonly_fields = ('post_photo', )
    prepopulated_fields = {'slug': ('title', )}  # ВАЖНО: slug не может быть одновременно и изменяемым, и автозаполняемым.
    filter_horizontal = ('tags', )  # Аналог filter_vertical.
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ('time_create', 'title')
    list_editable = ('is_published', )  # ВАЖНО: редактируемое поле не может быть кликабельным.
    list_per_page = 5
    actions = ('set_published', 'set_draft')
    search_fields = ('title', )  # ВАЖНО: искать возможно только по полям (т.е. по 'cat' поиск не осуществить напрямую,
    # ибо это внешний ключ). Если требуется всё же искать через категорию, то требуется указать поля связанной таблицы
    # либо люкапы: "cat__name" - поиск через категорию, "title__startswith" - поиск фрагмента только с начала строки.
    list_filter = (MarriedFilter, 'cat__name', 'is_published')
    save_on_top = True

    @admin.display(description='Изображение')
    def post_photo(self, women: Women) -> SafeString | str:
        """
        Функция отображения фото поста в админ-панели.

        :param women: Таблица women_women базы данных.
        :return: Неэкранированный HTML-тег или строку об отсутствии фото.
        """
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" width=50>')

        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request: HttpRequest, queryset) -> None:
        """
        Метод будет устанавливать статус публикации в состояние "опубликовано" для выбранных постов.

        :param request: Запрос пользователя.
        :param queryset: Менеджер модели, устанавливает is_published на "опубликовано".
        """
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request: HttpRequest, queryset) -> None:
        """
        Метод будет устанавливать статус публикации в состояние "черновик" для выбранных постов.

        :param request: Запрос пользователя.
        :param queryset: Менеджер модели, устанавливает is_published на "черновик".
        """
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} записей снято с публикации!', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Класс отвечает за настройку отображения отдельных категорий.

    Атрибуты:\n
    list_display - tuple - список отображаемых полей;\n
    list_display_links - tuple - список кликабельных полей;\n
    ordering - tuple - порядок сортировки.
    """
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    ordering = ('id', )


#  Регистрирование модели без декоратора - admin.site.register(Women, WomenAdmin)
