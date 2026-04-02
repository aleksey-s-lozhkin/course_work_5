import logging

from celery import shared_task
from django.utils import timezone

from .utils import format_habit_reminder, send_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder(habit_id):
    """Отправка напоминания о конкретной привычке"""
    from habits.models import Habit

    try:
        habit = Habit.objects.select_related('user').get(id=habit_id)
        user = habit.user

        if not user.telegram_chat_id:
            logger.info(f"У пользователя {user.email} не указан chat_id")
            return {'status': 'skipped', 'reason': 'no_chat_id'}

        message = format_habit_reminder(habit)
        success = send_telegram_message(user.telegram_chat_id, message)

        if success:
            logger.info(f"Напоминание отправлено для привычки '{habit.action}'")
            return {'status': 'sent', 'habit_id': habit_id}
        else:
            logger.error(f"Не удалось отправить напоминание для привычки {habit_id}")
            return {'status': 'failed', 'habit_id': habit_id}

    except Habit.DoesNotExist:
        logger.error(f"Привычка с id={habit_id} не найдена")
        return {'status': 'error', 'reason': 'habit_not_found'}
    except Exception as e:
        logger.error(f"Ошибка в send_habit_reminder: {e}")
        return {'status': 'error', 'reason': str(e)}


@shared_task
def send_habit_reminders():
    """Периодическая задача для отправки всех напоминаний"""
    from habits.models import Habit

    now = timezone.now()
    current_time = now.time()
    today = now.date()

    logger.info(f"Проверка напоминаний на {current_time}")

    # Находим привычки, которые нужно выполнить сейчас
    habits = Habit.objects.filter(
        time__lte=current_time,  # Время выполнения наступило или прошло
        is_pleasant=False,  # Напоминаем только о полезных привычках
    )

    sent_count = 0
    skipped_count = 0

    for habit in habits:
        # Проверяем периодичность
        last_notification = habit.updated_at.date()
        days_since = (today - last_notification).days

        if days_since >= habit.periodicity:
            # Отправляем напоминание
            send_habit_reminder.delay(habit.id)
            sent_count += 1

            # Обновляем время последнего напоминания
            habit.updated_at = now
            habit.save(update_fields=['updated_at'])
        else:
            skipped_count += 1

    logger.info(f"Отправлено напоминаний: {sent_count}, пропущено: {skipped_count}")

    return {'sent': sent_count, 'skipped': skipped_count, 'total': habits.count()}
