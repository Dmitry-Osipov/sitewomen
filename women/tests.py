from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from women.models import Women


# Create your tests here.
class GetPagesTestCase(TestCase):
    """
    Класс для тестирования получения страниц сайта приложения Women.

    Атрибуты:\n
    fixtures - list - фикстуры, который загружаются для каждого теста.
    """
    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']

    def setUp(self):
        """
        Инициализация перед выполнением каждого теста.
        """

    def test_mainpage(self):
        """
        Тест обращения к главной странице.
        """
        path = reverse('home')  # Путь к странице.
        response = self.client.get(path)  # Запрос клиента.
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Получение кода 200.
        # self.assertIn('women/index.html', response.template_name) - аналог этой функции прописан ниже.
        self.assertTemplateUsed('women/index.html')  # Использование шаблона в пути.
        self.assertEqual(response.context_data['title'], 'Главная страница')  # Проверка заголовка.

    def test_redirect_addpage(self):
        """
        Тест перенаправления со страницы добавления статьи для неавторизованных пользователей.
        """
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        """
        Тест получения данных главной страницы из БД.
        """
        w = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:5])

    def test_paginate_mainpage(self):
        """
        Тест проверяет работу пагинации главной страницы.
        """
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):
        """
        Проверка корректности отображения страницы с содержимым поста.
        """
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        """
        Действия после выполнения каждого теста.
        """
