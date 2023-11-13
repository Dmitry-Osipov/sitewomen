from django.contrib import admin
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
    list_per_page - int - максимальное количество отображаемых статей (пагинация реализуется автоматически).
    """
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    ordering = ('time_create', 'title')
    list_editable = ('is_published', )  # ВАЖНО: редактируемое поле не может быть кликабельным.
    list_per_page = 5


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
