from django.db import models
from django.conf import settings


class TelegramNotification(models.Model):
    """Модель для хранения истории уведомлений"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Пользователь'
    )
    habit = models.ForeignKey(
        'habits.Habit',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Привычка',
        null=True,
        blank=True
    )
    message = models.TextField(
        verbose_name='Текст сообщения'
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время отправки'
    )
    is_success = models.BooleanField(
        default=True,
        verbose_name='Успешно отправлено'
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='Ошибка'
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-sent_at']

    def __str__(self):
        return f"Уведомление для {self.user.username} от {self.sent_at}"