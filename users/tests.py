from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class RegisterUserTestCase(TestCase):
    """
    Класс предназначен для тестирования функционала регистрации.
    """
    def setUp(self):
        """
        Метод вызывается перед каждым тестом. В теле метода задаём словарь с данным как атрибут класса.
        """
        self.data = {
            'username': 'user_1',
            'email': 'user1@sitewomen.ru',
            'first_name': 'Dmitry',
            'last_name': 'Osipov',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }
    def test_form_registration_get(self):
        """
        Метод проверяет корректность отображения самой формы регистрации при GET-запросе.
        """
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_success(self):
        """
        Метод проверяет успешную регистрацию пользователя.
        """
        user_model = get_user_model()

        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_password_error(self):
        """
        Метод тестирует ошибки при регистрации пользователя.
        """
        self.data['password2'] = '12345678A'
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают')

    def test_user_registration_exists_error(self):
        """
        Проверка запрета на создание двух пользователей с одинаковыми логинами.
        """
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')
