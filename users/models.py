from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """
    Класс модели предназначен для расширения стандартной модели User.

    Атрибуты:\n
    photo - VARCHAR - необязательное поле фотографии;\n
    date_birth - DATETIME - необязательное поля дня рождения.
    """
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name='Фотография')
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')
