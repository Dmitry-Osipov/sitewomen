from django.apps import AppConfig


class WomenConfig(AppConfig):
    verbose_name = 'Женщины мира'  # Меняем название заголовка таблицы модели в админ-панели.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
