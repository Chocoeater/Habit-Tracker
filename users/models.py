from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail", help_text="Введите адрес электронной почты")
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='имя пользователя',
        help_text='Введите имя пользователя'
    )
    telegram_id = models.CharField(
        max_length=150,
        verbose_name='ID чата',
        help_text='Введите Ваш ID чата',
        blank=True,
        null=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f'{self.username} -- {self.email}'
