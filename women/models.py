from django.db import models

# Create your models here.
class Women(models.Model):
    """
    Класс является связкой для ORM с одноимённой таблицей в БД. Наследование от Model делает наш класс классом модели.

    Атрибуты:\n
    id - PRIMARY KEY, INTEGER, AUTOINCREMENT - главный ключ, формируется автоматически;\n
    title - VARCHAR - обязательное текстовое поле (содержит одну сроку) заголовка (имя женщины), максимальная длина -
    255 символов;\n
    content - TEXT - необязательное (blank=True) текстовое поле (содержит целое текстовое поле) c содержимым статьи;\n
    time_create - DATETIME - обязательное поле, содержащее время добавления записи в БД, во время первого появления
    конкретной записи автоматически проставляет время (auto_now_add=True);\n
    time_update - DATETIME - обязательное поле, содержащее время обновление записи в БД, автоматически обновляет время
    изменения конкретной записи в БД (auto_now=True);\n
    is_published - BOOLEAN - обязательное поле показывает, опубликована ли статья, по умолчанию все статьи публикуются.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        """
        Вложенный класс предназначен для фильтрации данных.

        Атрибуты:\n
        ordering - list - определяет порядок сортировки выбранных записей модели;\n
        indexes - list - определяет столбцы, записи которых должны быть пронумерованы.
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
