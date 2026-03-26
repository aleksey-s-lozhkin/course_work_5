# habits/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from .validators import HabitValidators


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related',
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность (дни)'
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )
    execution_time = models.PositiveSmallIntegerField(
        verbose_name='Время на выполнение (сек)'
    )
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def clean(self):
        """Валидация на уровне модели (вызывается при full_clean())"""
        HabitValidators.validate_all(self)

    def save(self, *args, **kwargs):
        """Переопределяем save для автоматической валидации"""
        self.full_clean()  # Вызывает clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}: {self.action} в {self.time}"