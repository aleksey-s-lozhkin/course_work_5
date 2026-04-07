import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не настроен")
        return False

    if not chat_id:
        logger.error("chat_id не указан")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        if result.get('ok'):
            logger.info(f"Сообщение отправлено в chat_id={chat_id}")
            return True
        else:
            logger.error(f"Telegram API ошибка: {result}")
            return False

    except requests.exceptions.Timeout:
        logger.error("Таймаут при отправке сообщения")
        return False
    except requests.exceptions.ProxyError as e:
        logger.error(f"Ошибка SOCKS5 прокси: {e}")
        return False
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Ошибка подключения: {e}")
        return False
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return False


def format_habit_reminder(habit):
    """Форматирование напоминания о привычке"""
    message = "<b>Напоминание о привычке!</b>\n\n"
    message += f"<b>Действие:</b> {habit.action}\n"
    message += f"<b>Место:</b> {habit.place}\n"
    message += f"<b>Время:</b> {habit.time.strftime('%H:%M')}\n"
    message += f"<b>Периодичность:</b> {habit.periodicity} день(дней)\n"
    message += f"<b>Время на выполнение:</b> {habit.execution_time} сек\n"

    if habit.reward:
        message += f"<b>Вознаграждение:</b> {habit.reward}\n"
    elif habit.related_habit:
        message += f"<b>После выполнения:</b> {habit.related_habit.action}\n"

    return message
