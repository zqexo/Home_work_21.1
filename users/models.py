from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='Почта')
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
