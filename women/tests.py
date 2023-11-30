from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class GetPagesTestCase(TestCase):
    """
    Класс для тестирования получения страниц сайта приложения Women.
    """
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

    def tearDown(self):
        """
        Действия после выполнения каждого теста.
        """
