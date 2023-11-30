from django.contrib.sitemaps import Sitemap

from women.models import Women, Category


class PostSitemap(Sitemap):
    """
    Класс служит для формирования данных карты сайта по постам.

    Атрибуты:\n
    changefreq - str - частота обновления страниц;\n
    priority - float - приоритет.
    """
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        """
        Метод возвращает все те записи, которые попадут в карту сайта.

        :return: Все опубликованные записи.
        """
        return Women.published.all()

    def lastmod(self, obj):
        """
        Метод возвращает время последнего изменения страницы.

        :param obj: Ссылка на записи модели Women.
        :return: Время последнего изменения страницы.
        """
        return obj.time_update


class CategorySitemap(Sitemap):
    """
    Класс служит для формирования данных карты сайта по категориям.

    Атрибуты:\n
    changefreq - str - частота обновления страниц;\n
    priority - float - приоритет.
    """
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        """
        Метод возвращает все те записи, которые попадут в карту сайта.

        :return: Все опубликованные записи.
        """
        return Category.objects.all()
