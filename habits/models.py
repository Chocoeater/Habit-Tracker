from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        related_name="habits",
        verbose_name="привычка",
        on_delete=models.CASCADE
    )
    place = models.CharField(
        max_length=100,
        verbose_name="место выполнения",
        help_text="Введите место, в котором необходимо выполнять привычку"
    )
    time_to_do = models.TimeField(
        verbose_name='время выполнения',
        help_text='Введите время, когда необходимо выполнять привычку'
    )
    action = models.CharField(
        max_length=500,
        verbose_name='действие',
        help_text='Введите действие, которое представляет собой привычка'
    )
    frequency = models.PositiveIntegerField(
        default=1,
        verbose_name='периодичность (в днях)',
        help_text='Задайте периодичность повторения привычки (в днях)'
    )
    tag_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name='признак приятной привычки',
        help_text='Привычка является приятной?'
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='связанная привычка',
        help_text='Задайте привычку-вознаграждение'
    )
    reward = models.CharField(
        max_length=300,
        verbose_name='вознаграждение',
        help_text='Введите вознаграждение',
        null=True,
        blank=True
    )
    duration = models.PositiveIntegerField(
        verbose_name='время на выполнение (в секундах)',
        help_text='Задайте время на выполнение привычки (в секундах)'
    )
    tag_public = models.BooleanField(
        default=True,
        verbose_name='признак публичности',
        help_text='Могут ли другие пользователи видеть привычку?'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'Привычка №{self.pk} -- {self.action}'