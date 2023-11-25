from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    """
    Класс отвечает за авторизацию пользователя по почте и паролю.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Метод осуществляет аутентификацию по почте и паролю.

        :param request: Запрос.
        :param username: Почта клиента.
        :param password: Пароль клиента.
        :return: Объект пользователя или значение None.
        :raises DoesNotExist: Пользователь отсутствует в БД.
        :raises MultipleObjectsReturned: Возврат более 1 модели пользователя.
        """
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user

            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Функция отвечает за отображение пользователя в системе.

        :param user_id: pk из БД конкретного пользователя.
        :return: Объект пользователя или значение None.
        :raises DoesNotExist: Пользователь отсутствует в БД.
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
