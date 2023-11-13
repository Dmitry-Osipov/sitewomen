from django.contrib import admin, messages
from django.http import HttpRequest

from .models import Women, Category

# Register your models here.
@admin.register(Women)  # Регистрируем модель.
class WomenAdmin(admin.ModelAdmin):
    """
    Класс отвечает за настройку отображения отдельных статей.

    Атрибуты:\n
    list_display - tuple - список полей, которые требуется отобразить;\n
    list_display_links - tuple - список полей, по которым можно перейти на конкретный пост;\n
    ordering - tuple - порядок сортировки (если указано 2 и более поля, то сначала будет сортироваться по первому полю,
    а затем, если будут совпадения, то по второму полю);\n
    list_editable - tuple - список полей, которые можно редактировать;\n
    list_per_page - int - максимальное количество отображаемых статей (пагинация реализуется автоматически);\n
    actions - tuple - список действий (посредством функций).
    """
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title', )
    ordering = ('time_create', 'title')
    list_editable = ('is_published', )  # ВАЖНО: редактируемое поле не может быть кликабельным.
    list_per_page = 5
    actions = ('set_published', 'set_draft')

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, women: Women) -> str:
        """
        Метод отвечает за создание дополнительного поля с указанием длины блока content конкретной записи. Дополнительное
        поле в БД отсутствует и не сохраняется туда.

        :param women: Таблица women_women базы данных.
        :return: Дополнительное поле с информацией о количестве символов блока content конкретной записи.
        """
        return f'Описание {len(women.content)} символов.'

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
