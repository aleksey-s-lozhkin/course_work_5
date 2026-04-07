from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from habits.models import Habit
from telegram.tasks import send_habit_reminder, send_habit_reminders

User = get_user_model()


class TelegramTasksTest(TestCase):
    """Тесты для задач Celery"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', username='testuser', password='testpass123', telegram_chat_id='123456789'
        )
        self.habit = Habit.objects.create(
            user=self.user, place='Дом', time='12:00:00', action='Тестовая привычка', execution_time=60, periodicity=1
        )

    @patch('telegram.tasks.send_telegram_message')
    def test_send_habit_reminder_success(self, mock_send):
        """Тест успешной отправки напоминания"""
        mock_send.return_value = True
        result = send_habit_reminder(self.habit.id)
        self.assertEqual(result['status'], 'sent')

    @patch('telegram.tasks.send_telegram_message')
    def test_send_habit_reminder_no_chat_id(self, mock_send):
        """Тест: нет chat_id у пользователя"""
        self.user.telegram_chat_id = None
        self.user.save()
        result = send_habit_reminder(self.habit.id)
        self.assertEqual(result['status'], 'skipped')
        self.assertEqual(result['reason'], 'no_chat_id')

    def test_send_habit_reminder_habit_not_found(self):
        """Тест: привычка не найдена"""
        result = send_habit_reminder(99999)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['reason'], 'habit_not_found')

    @patch('telegram.tasks.send_habit_reminder.delay')
    def test_send_habit_reminders(self, mock_delay):
        """Тест периодической задачи"""
        mock_delay.return_value = None
        result = send_habit_reminders()
        self.assertIn('sent', result)
        self.assertIn('skipped', result)


class TelegramUtilsTest(TestCase):
    """Тесты для утилит Telegram"""

    @patch('telegram.utils.requests.post')
    @override_settings(TELEGRAM_BOT_TOKEN='test_token')  # ✅ Добавлен временный токен
    def test_send_telegram_message_success(self, mock_post):
        """Тест успешной отправки сообщения"""
        from telegram.utils import send_telegram_message

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ok': True}
        mock_post.return_value = mock_response

        result = send_telegram_message('123456789', 'Тест')
        self.assertTrue(result)

    @patch('telegram.utils.requests.post')
    @override_settings(TELEGRAM_BOT_TOKEN=None)  # ✅ Без токена
    def test_send_telegram_message_no_token(self, mock_post):
        """Тест: нет токена"""
        from telegram.utils import send_telegram_message

        result = send_telegram_message('123456789', 'Тест')
        self.assertFalse(result)

    @patch('telegram.utils.requests.post')
    @override_settings(TELEGRAM_BOT_TOKEN='test_token')
    def test_send_telegram_message_no_chat_id(self, mock_post):
        """Тест: нет chat_id"""
        from telegram.utils import send_telegram_message

        result = send_telegram_message(None, 'Тест')
        self.assertFalse(result)

    @patch('telegram.utils.requests.post')
    @override_settings(TELEGRAM_BOT_TOKEN='test_token')
    def test_send_telegram_message_timeout(self, mock_post):
        """Тест: таймаут"""
        import requests

        from telegram.utils import send_telegram_message

        mock_post.side_effect = requests.exceptions.Timeout()

        result = send_telegram_message('123456789', 'Тест')
        self.assertFalse(result)
